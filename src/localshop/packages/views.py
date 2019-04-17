import logging
from wsgiref.util import FileWrapper

from braces.views import CsrfExemptMixin
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.db.models import Q
from django.http import (
    Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden,
    HttpResponseNotFound)
from django.shortcuts import redirect
from django.utils import six
from django.views import generic
from versio.version import Version
from versio.version_scheme import (
    Pep440VersionScheme, Simple3VersionScheme, Simple4VersionScheme)

from localshop.packages import models
from localshop.packages import forms
from localshop.packages.mixins import RepositoryMixin
from localshop.packages.pypi import get_search_names
from localshop.packages.tasks import fetch_package
from localshop.packages.utils import (
    alter_old_distutils_request, get_versio_versioning_scheme)
from localshop.permissions.mixins import RepositoryAccessMixin
from localshop.utils import enqueue

logger = logging.getLogger(__name__)
Version.set_supported_version_schemes((
    Simple3VersionScheme, Simple4VersionScheme, Pep440VersionScheme,))


class SimpleIndex(CsrfExemptMixin, RepositoryMixin, RepositoryAccessMixin,
                  generic.ListView):
    """Index view with all available packages used by /simple url

    This page is used by pip/easy_install to find packages.

    """
    context_object_name = 'packages'
    http_method_names = ['get', 'post']
    template_name = 'packages/simple_package_list.html'

    def post(self, request, repo):
        alter_old_distutils_request(request)

        actions = {
            'submit': handle_register_or_upload,
            'file_upload': handle_register_or_upload,
        }
        action = request.POST.get(':action')

        handler = actions.get(action)
        if not handler:
            return HttpResponseNotFound('Unknown action: %s' % action)

        if not request.user.is_authenticated and not request.credentials:
            return HttpResponseForbidden(
                "You need to be authenticated to upload packages")

        # Both actions currently are upload actions, so check is simple
        if request.credentials and not request.credentials.allow_upload:
            return HttpResponseForbidden(
                "Upload is not allowed with the provided credentials")

        return handler(
            request.POST, request.FILES, request.user, self.repository)

    def get_queryset(self):
        return self.repository.packages.all()


class SimpleDetail(RepositoryMixin, RepositoryAccessMixin, generic.DetailView):
    """List all available files for a specific package.

    This page is used by pip/easy_install to find the files.
    """
    model = models.Package
    context_object_name = 'package'
    template_name = 'packages/simple_package_detail.html'

    def get(self, request, repo, slug):
        condition = Q()
        for name in get_search_names(slug):
            condition |= Q(name__iexact=name)

        try:
            package = self.repository.packages.get(condition)
        except ObjectDoesNotExist:
            if not self.repository.enable_auto_mirroring:
                raise Http404("Auto mirroring is not enabled")

            enqueue(fetch_package, self.repository.pk, slug)
            return redirect(self.repository.upstream_pypi_url + '/' + slug)

        # Redirect if slug is not an exact match
        if slug != package.name:
            url = reverse('packages:simple_detail', kwargs={
                'repo': self.repository.slug,
                'slug': package.name
            })
            return redirect(url)

        self.object = package
        context = self.get_context_data(
            object=self.object,
            releases=list(package.releases.all()))
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['base_url'] = self.request.build_absolute_uri('/')[:-1]
        return ctx


class DownloadReleaseFile(RepositoryMixin, RepositoryAccessMixin,
                          generic.View):
    """
    If the requested file is not already cached locally from a previous
    download it will be fetched from PyPi for local storage and the client will
    be redirected to PyPi, unless the LOCALSHOP_ISOLATED variable is set to
    True, in which case the file will be served to the client after it is
    downloaded.
    """
    def get(self, request, repo, name, pk, filename):
        release_file = models.ReleaseFile.objects.get(pk=pk)
        if not release_file.file_is_available:

            if not self.repository.enable_auto_mirroring:
                raise Http404("Auto mirroring is not enabled")

            logger.info("Queueing %s for mirroring", release_file.url)
            release_file.download()
            if not settings.LOCALSHOP_ISOLATED:
                logger.debug("Redirecting user to pypi")
                return redirect(release_file.url)
            else:
                release_file = models.ReleaseFile.objects.get(pk=pk)

        if settings.MEDIA_URL:
            return redirect(release_file.distribution.url)

        # TODO: Use sendfile if enabled
        response = HttpResponse(
            FileWrapper(release_file.distribution.file),
            content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % (
            release_file.filename)
        size = release_file.distribution.file.size
        if size:
            response["Content-Length"] = size
        return response


def handle_register_or_upload(post_data, files, user, repository):
    """Process a `register` or `upload` comment issued via distutils.

    This method is called with the authenticated user.

    """
    name = post_data.get('name')
    version = post_data.get('version')

    if settings.LOCALSHOP_VERSIONING_TYPE:
        scheme = get_versio_versioning_scheme(settings.LOCALSHOP_VERSIONING_TYPE)
        try:
            Version(version, scheme=scheme)
        except AttributeError:
            response = HttpResponseBadRequest(
                reason="Invalid version supplied '{!s}' for '{!s}' scheme.".format(
                    version, settings.LOCALSHOP_VERSIONING_TYPE))
            return response

    if not name or not version:
        logger.info("Missing name or version for package")
        return HttpResponseBadRequest('No name or version given')

    try:
        condition = Q()
        for search_name in get_search_names(name):
            condition |= Q(name__iexact=search_name)

        package = repository.packages.get(condition)

        # Error out when we try to override a mirror'ed package for now
        # not sure what the best thing is
        if not package.is_local:
            return HttpResponseBadRequest(
                '%s is a pypi package!' % package.name)

        try:
            release = package.releases.get(version=version)
        except ObjectDoesNotExist:
            release = None
    except ObjectDoesNotExist:
        package = None
        release = None

    # Validate the data
    form = forms.ReleaseForm(post_data, instance=release)
    if not form.is_valid():
        return HttpResponseBadRequest(reason=form.errors.values()[0][0])

    if not package:
        pkg_form = forms.PackageForm(post_data, repository=repository)
        if not pkg_form.is_valid():
            return HttpResponseBadRequest(
                reason=six.next(six.itervalues(pkg_form.errors))[0])
        package = pkg_form.save()

    release = form.save(commit=False)
    release.package = package
    release.save()

    # If this is an upload action then process the uploaded file
    if files:
        files = {
            'distribution': files['content']
        }
        filename = files['distribution']._name
        try:
            release_file = release.files.get(filename=filename)
            if settings.LOCALSHOP_RELEASE_OVERWRITE is False:
                message = 'That it already released, please bump version.'
                return HttpResponseBadRequest(message)
        except ObjectDoesNotExist:
            release_file = models.ReleaseFile(
                release=release, filename=filename)

        form_file = forms.ReleaseFileForm(
            post_data, files, instance=release_file)
        if not form_file.is_valid():
            return HttpResponseBadRequest('ERRORS %s' % form_file.errors)
        release_file = form_file.save(commit=False)
        release_file.save()

    return HttpResponse()
