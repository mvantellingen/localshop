import base64
import logging

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from localshop.utils import permission_required
from localshop.packages import forms
from localshop.packages import models
from localshop.packages import tasks
from localshop.packages.pypi import get_package_data
from localshop.packages.utils import parse_distutils_request, validate_client

logger = logging.getLogger(__name__)


@validate_client
class SimpleIndex(ListView):
    """Index view with all available packages used by /simple url

    This page is used by pip/easy_install to find packages.

    """
    queryset = models.Package.objects.values('name')
    context_object_name = 'packages'
    http_method_names = ['get', 'post']
    template_name = 'packages/simple_package_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SimpleIndex, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        data, files = parse_distutils_request(request)

        # XXX: Auth is currently a bit of a hack
        auth = request.META.get('HTTP_AUTHORIZATION')
        if not auth:
            response = HttpResponse('Missing auth header')
            response.status_code = 401
            return response
        method, identity = auth.split()
        username, password = base64.decodestring(identity).split(':')
        user = authenticate(username=username, password=password)
        if not user:
            response = HttpResponse('Invalid username/password')
            response.status_code = 401
            return response

        actions = {
            'submit': handle_register_or_upload,
            'file_upload': handle_register_or_upload,
        }

        handler = actions.get(data.get(':action'))
        if not handler:
            raise Http404('Unknown action')
        return handler(data, files, user)


@validate_client
class SimpleDetail(DetailView):
    """List all available files for a specific package.

    This page is used by pip/easy_install to find the files.

    """
    model = models.Package
    context_object_name = 'package'
    template_name = 'packages/simple_package_detail.html'

    def get(self, request, slug):
        try:
            package = models.Package.objects.get(name__iexact=slug)
        except ObjectDoesNotExist:
            package = get_package_data(slug)

        self.object = package
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


@permission_required('packages.view_package')
class Index(ListView):
    model = models.Package
    context_object_name = 'packages'


@permission_required('packages.view_package')
class Detail(DetailView):
    model = models.Package
    context_object_name = 'package'
    slug_url_kwarg = 'name'
    slug_field = 'name'

    def get_object(self, queryset=None):
        # Could be dropped when we use django 1.4
        self.kwargs['slug'] = self.kwargs.get(self.slug_url_kwarg, None)
        return super(Detail, self).get_object(queryset)

    def get_context_data(self, *args, **kwargs):
        context = super(Detail, self).get_context_data(*args, **kwargs)
        context['release'] = self.object.last_release
        return context


@permission_required('packages.change_package')
def refresh(request, name):
    try:
        package = models.Package.objects.get(name__iexact=name)
    except ObjectDoesNotExist:
        package = None
    package = get_package_data(name, package)
    return redirect(package)


@validate_client
def download_file(request, name, pk, filename):
    """Redirect the client to the pypi hosted file if the file is not
    mirror'ed yet (and isn't a local package).  Otherwise serve the file.

    """
    release_file = models.ReleaseFile.objects.get(pk=pk)
    if not release_file.distribution:
        logger.info("Queueing %s for mirroring", release_file.url)
        tasks.download_file.delay(pk=release_file.pk)
        return redirect(release_file.url)

    # TODO: Use sendfile if enabled
    response = HttpResponse(release_file.distribution.file,
        content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % (
        release_file.filename)
    return response


def handle_register_or_upload(post_data, files, user):
    """Process a `register` or `upload` comment issued via distutils.

    This method is called with the authenticated user.

    """
    name = post_data.get('name')
    version = post_data.get('version')
    if not name or not version:
        logger.info("Missing name or version for package")
        return HttpResponseBadRequest('No name or version given')

    try:
        package = models.Package.objects.get(name=name)

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
