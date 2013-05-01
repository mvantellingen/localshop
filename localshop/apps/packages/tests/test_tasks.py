import mock
from django.test import TestCase

from localshop.apps.packages import tasks
from localshop.apps.packages import models


class TestTasks(TestCase):
    def test_download_file(self):
        package = models.Package.objects.create(name='localshop')
        release = models.Release.objects.create(package=package, version='0.1')
        release_file = models.ReleaseFile.objects.create(
            release=release,
            md5_digest='098f6bcd4621d373cade4e832627b4f6',
            python_version='source',
            url=(
                'http://pypi.python.org/packages/source/l/localshop/'
                'localshop-0.1.tar.gz'
            )
        )

        with mock.patch('requests.get') as mock_obj:
            mock_obj.return_value = mock.Mock()
            mock_obj.return_value.content = 'test'
            mock_obj.return_value.headers = {
                'content-length': 1024
            }
            tasks.download_file(release_file.pk)

        release_file = models.ReleaseFile.objects.get(pk=release_file.pk)
        self.assertEqual(release_file.distribution.read(), 'test')

        self.assertEqual(
            release_file.distribution.name,
            'source/l/localshop/localshop-0.1.tar.gz')

    def test_download_file_incorrect_md5_sum(self):
        package = models.Package.objects.create(name='localshop')
        release = models.Release.objects.create(package=package, version='0.1')
        release_file = models.ReleaseFile.objects.create(
            release=release,
            md5_digest='098f6bcd4621d373cade4e832627b4f6',
            python_version='source',
            url=(
                'http://pypi.python.org/packages/source/l/localshop/'
                'localshop-0.1.tar.gz'
            )
        )

        with mock.patch('requests.get') as mock_obj:
            mock_obj.return_value = mock.Mock()
            mock_obj.return_value.content = 'tes.'
            mock_obj.return_value.headers = {
                'content-length': 1024
            }
            tasks.download_file(release_file.pk)

        release_file = models.ReleaseFile.objects.get(pk=release_file.pk)
        self.assertFalse(release_file.distribution)
