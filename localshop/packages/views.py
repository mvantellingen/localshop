import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from localshop.packages import forms
from localshop.packages import models
from localshop.packages import tasks
from localshop.packages.pypi import get_package_urls
from localshop.packages.utils import parse_distutils_request

logger = logging.getLogger(__name__)


class SimpleIndex(ListView):
    model = models.Package
    http_method_names = ['get', 'post']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SimpleIndex, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        data, files = parse_distutils_request(request)

        actions = {
            'submit': handle_register_or_upload,
            'file_upload': handle_register_or_upload,
        }

        handler = actions.get(data.get(':action'))
        if not handler:
            raise Http404('Unknown action')
        return handler(data, files)


class SimpleDetail(DetailView):
    model = models.Package

    def get(self, request, slug):
        try:
            package = models.Package.objects.get(name__iexact=slug)
        except ObjectDoesNotExist:
            package = get_package_urls(slug)

        self.object = package
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


def download_file(request, pk, filename):
    release_file = models.ReleaseFile.objects.get(pk=pk)
    if not release_file.file:
        logger.info("Queueing %s for mirroring", release_file.url)
        tasks.download_file.delay(pk=release_file.pk)
        return redirect(release_file.url)

    return redirect(release_file.file.url)


def handle_register_or_upload(post_data, files):
    name = post_data.get('name')
    if not name:
        return HttpResponseBadRequest('No name given')
    version = post_data.get('version')
    if not version:
        return HttpResponseBadRequest('No version given')

    try:
        package = models.Package.objects.get(name=name)

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
        return HttpResponseBadRequest('ERRORS %s' % form.errors)

    if not package:
        package = models.Package(name=name, is_local=True)
        package.save()

    release = form.save(commit=False)
    release.package = package
    release.save()

    if files:
        filename = files['distribution']._name
        try:
            release_file = release.files.get(filename=filename)
        except ObjectDoesNotExist:
            release_file = models.ReleaseFile(
                release=release, filename=filename)

        form_file = forms.ReleaseFileForm(
            post_data, files, instance=release_file)
        if not form_file.is_valid():
            return HttpResponseBadRequest('ERRORS %s' % form_file.errors)
        form_file.save()

    return HttpResponse()
