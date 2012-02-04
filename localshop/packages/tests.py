from django.test import TestCase
from localshop.packages import utils
from localshop.packages import tasks
from localshop.packages import models


class UtilsTest(TestCase):
    def test_get_package_urls(self):
        pass

    def test_download_file(self):
        package = models.Package(name='test-package')
        package.save()

        release = models.Release(
            package=package, version='0.1')
        release.save()

        release_file = models.ReleaseFile(
            release=release,
            url='http://pypi.python.org/packages/source/p/pip/pip-0.3.tar.gz'
        )
        release_file.save()

        tasks.download_file(release_file.pk)

        release_file = models.ReleaseFile.objects.get(pk=release_file.pk)
