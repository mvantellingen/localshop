import logging
import os
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.decorators.cache import cache_page

from versio.version import Version
from versio.version_scheme import Pep440VersionScheme, Simple3VersionScheme, Simple4VersionScheme, PerlVersionScheme

from localshop.utils import enqueue
from localshop.apps.packages import forms, models
from localshop.apps.packages.tasks import fetch_package
from localshop.apps.packages.pypi import get_search_names
from localshop.apps.packages.signals import release_file_notfound
from localshop.apps.packages.utils import parse_distutils_request, get_versio_versioning_scheme
from localshop.apps.permissions.utils import credentials_required
from localshop.apps.permissions.utils import split_auth, authenticate_user
from localshop.http import HttpResponseUnauthorized
from localshop.views import LoginRequiredMixin, PermissionRequiredMixin

logger = logging.getLogger(__name__)
Version.set_supported_version_schemes((Simple3VersionScheme, Simple4VersionScheme, Pep440VersionScheme,))


class SimpleIndex(ListView):
    """Index view with all available packages used by /simple url

    This page is used by pip/easy_install to find packages.

    """
    queryset = models.Package.objects.values('name')
    context_object_name = 'packages'
    http_method_names = ['get', 'post']
    template_name = 'packages/simple_package_list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(credentials_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SimpleIndex, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        parse_distutils_request(request)

        # XXX: Auth is currently a bit of a hack
        method, identity = split_auth(request)
        if not method:
            return HttpResponseUnauthorized(content='Missing auth header')

        user = authenticate_user(request)
        if not user:
            return HttpResponse('Invalid username/password', status=401)

        actions = {
            'submit': handle_register_or_upload,
            'file_upload': handle_register_or_upload,
        }

        handler = actions.get(request.POST.get(':action'))
        if not handler:
            return HttpResponseNotFound('Unknown action')
        return handler(request.POST, request.FILES, user)

simple_index = SimpleIndex.as_view()


class SimpleDetail(DetailView):
    """List all available files for a specific package.

    This page is used by pip/easy_install to find the files.
    """
    model = models.Package
    context_object_name = 'package'
    template_name = 'packages/simple_package_detail.html'

    @method_decorator(credentials_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SimpleDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, slug):
        condition = Q()
        for name in get_search_names(slug):
            condition |= Q(name__iexact=name)

        try:
            package = models.Package.objects.get(condition)
        except ObjectDoesNotExist:
            enqueue(fetch_package, slug)
            return redirect('https://pypi.python.org/simple/{}'.format(slug))

        # Redirect if slug is not an exact match
        if slug != package.name:
            url = reverse('packages-simple:simple_detail',
                          kwargs={'slug': package.name})
            return redirect(url)

        self.object = package
        context = self.get_context_data(
            object=self.object,
            releases=list(package.releases.all()))
        return self.render_to_response(context)

simple_detail = cache_page(60)(SimpleDetail.as_view())


class Index(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Package
    context_object_name = 'packages'
    permission_required = 'packages.view_package'


class Detail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Package
    context_object_name = 'package'
    slug_url_kwarg = 'name'
    slug_field = 'name'
    permission_required = 'packages.view_package'

    def get_object(self, queryset=None):
        # Could be dropped when we use django 1.4
        self.kwargs['slug'] = self.kwargs.get(self.slug_url_kwarg, None)
        return super(Detail, self).get_object(queryset)

    def get_context_data(self, *args, **kwargs):
        context = super(Detail, self).get_context_data(*args, **kwargs)
        context['release'] = self.object.last_release
        context['pypi_url'] = settings.LOCALSHOP_PYPI_URL
        return context


@permission_required('packages.change_package')
@login_required
def refresh(request, name):
    try:
        package = models.Package.objects.get(name__iexact=name)
    except ObjectDoesNotExist:
        package = None
        enqueue(fetch_package, name)
    return redirect(package)


@credentials_required
def download_file(request, name, pk, filename):
    """
    If the requested file is not already cached locally from a previous
    download it will be fetched from PyPi for local storage and the client will
    be redirected to PyPi, unless the LOCALSHOP_ISOLATED variable is set to
    True, in which case the file will be served to the client after it is
    downloaded.
    """

    release_file = models.ReleaseFile.objects.get(pk=pk)
    if not release_file.distribution or not os.path.isfile(release_file.distribution.path):
        logger.info("Queueing %s for mirroring", release_file.url)
        release_file_notfound.send(sender=release_file.__class__,
                                   release_file=release_file)
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


def handle_register_or_upload(post_data, files, user):
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
                reason='Invalid version supplied {!r} for {!r} scheme.'.format(
                    version, settings.LOCALSHOP_VERSIONING_TYPE))
            return response

    if not name or not version:
        logger.info("Missing name or version for package")
        return HttpResponseBadRequest('No name or version given')

    try:
        condition = Q()
        for search_name in get_search_names(name):
            condition |= Q(name__iexact=search_name)

        package = models.Package.objects.get(condition)

        # Error out when we try to override a mirror'ed package for now
        # not sure what the best thing is
        if not package.is_local:
            return HttpResponseBadRequest(
                '%s is a pypi package!' % package.name)

        # Ensure that the user is one of the owners
        if not package.owners.filter(pk=user.pk).exists():
            if not user.is_superuser:
                return HttpResponseForbidden('No permission for this package')

            # User is a superuser, add him to the owners
            package.owners.add(user)

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
        return HttpResponseBadRequest('ERRORS %s' % form.errors)

    if not package:
        package = models.Package.objects.create(name=name, is_local=True)
        package.owners.add(user)
        package.save()

    release = form.save(commit=False)
    release.package = package
    release.user = user
    release.save()

    # If this is an upload action then process the uploaded file
    if files:
        filename = files['distribution']._name
        try:
            release_file = release.files.get(filename=filename)
            if settings.LOCALSHOP_RELEASE_OVERWRITE is False:
                message = 'That it already released, please bump version.'
                return HttpResponseBadRequest(message)
        except ObjectDoesNotExist:
            release_file = models.ReleaseFile(
                release=release, filename=filename, user=user)

        form_file = forms.ReleaseFileForm(
            post_data, files, instance=release_file)
        if not form_file.is_valid():
            return HttpResponseBadRequest('ERRORS %s' % form_file.errors)
        release_file = form_file.save(commit=False)
        release_file.user = user
        release_file.save()

    return HttpResponse()
