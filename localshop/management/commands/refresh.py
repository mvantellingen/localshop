from django.core.management.base import BaseCommand

from ...apps.packages.models import Package
from ...apps.packages.pypi import get_package_data


class Command(BaseCommand):
    help = "refreshes (downloads new versions) all packages from pypi"

    def handle(self, *args, **kwargs):
        for package in Package.objects.filter(is_local=False):
            get_package_data(package.name, package)
