import mock
from cStringIO import StringIO
from django.test import TestCase
from requests.packages.urllib3.response import HTTPResponse

from localshop.apps.packages import utils
from localshop.apps.packages import tasks
from localshop.apps.packages import models


class TestTasks(TestCase):
    def test_download_file(self):
        package = models.Package(name='localshop')
        package.save()

        release = models.Release(
            package=package, version='0.1')
        release.save()

        release_file = models.ReleaseFile(
            release=release,
            python_version='source',
            url='http://pypi.python.org/packages/source/l/localshop/' \
                'localshop-0.1.tar.gz'
        )
        release_file.save()

        with mock.patch('requests.get') as mock_obj:
            mock_obj.return_value = mock.Mock()
            mock_obj.return_value.content = b'1a2b3c'
            tasks.download_file(release_file.pk)

        release_file = models.ReleaseFile.objects.get(pk=release_file.pk)
        self.assertEqual(release_file.distribution.read(), b'1a2b3c')

        self.assertEqual(release_file.distribution.name,
            'source/l/localshop/localshop-0.1.tar.gz')
