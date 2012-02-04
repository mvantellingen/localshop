from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import redirect

from localshop.packages import models
from localshop.packages.utils import get_package_urls


class SimpleIndex(ListView):
    model = models.Package


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
    file = models.ReleaseFile.objects.get(pk=pk)
    return redirect(file)
