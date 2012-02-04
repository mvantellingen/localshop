import datetime
import mock
from django.test import TestCase

from localshop.packages import models


class TestPypi(TestCase):
    def test_get_package_urls_new(self):
        from localshop.packages.pypi import get_package_urls

        with mock.patch('xmlrpclib.ServerProxy') as mock_obj:
            mock_obj.return_value = client = mock.Mock()
            client.package_releases.return_value = ['0.1', '0.2']

            def side_effect(name, version):
                return [{
                    'comment_text': '',
                    'downloads': 1,
                    'filename': 'localshop-%s.tar.gz' % version,
                    'has_sig': True,
                    'md5_digest': '7ddf32e17a6ac5ce04a8ecbf782ca509',
                    'packagetype': 'sdist',
                    'python_version': 'source',
                    'size': 23232,
                    'upload_time': datetime.datetime(2012, 2, 2, 11, 32, 00),
                    'url': 'http://pypi.python.org/packages/source/r/'
                        'localshop/localshop-%s.tar.gz' % version
                }]
            client.package_urls.side_effect = side_effect

            package = get_package_urls('localshop')

        package = models.Package.objects.get(pk=package.pk)

        self.assertEqual(package.releases.count(), 2)
        self.assertTrue(package.releases.get(version='0.1'))
        self.assertTrue(package.releases.get(version='0.2'))

        self.assertEqual(package.releases.get(version='0.1').files.count(), 1)
        self.assertEqual(package.releases.get(version='0.2').files.count(), 1)

        info = package.releases.get(version='0.1').files.all()[0]
        self.assertEqual(info.filename, 'localshop-0.1.tar.gz')
        self.assertEqual(info.type, 'sdist')
        self.assertEqual(info.python_version, 'source')
        self.assertEqual(info.digest, '7ddf32e17a6ac5ce04a8ecbf782ca509')
        self.assertEqual(info.size, 23232)
        self.assertEqual(info.url, 'http://pypi.python.org/packages/source/r/'
            'localshop/localshop-0.1.tar.gz')

    def test_get_package_urls_wrong_case(self):
        from localshop.packages.pypi import get_package_urls

        with mock.patch('xmlrpclib.ServerProxy') as mock_obj:
            mock_obj.return_value = client = mock.Mock()

            def se_package_releases(name, show_hidden=False):
                """side_effect for package_releases"""
                if name == 'localshop':
                    return ['0.1']
                return []
            client.package_releases.side_effect = se_package_releases

            client.search.return_value = [
                {'name': 'localshop'}
            ]

            client.package_urls.return_value = [{
                    'comment_text': '',
                    'downloads': 1,
                    'filename': 'localshop-0.1.tar.gz',
                    'has_sig': True,
                    'md5_digest': '7ddf32e17a6ac5ce04a8ecbf782ca509',
                    'packagetype': 'sdist',
                    'python_version': 'source',
                    'size': 23232,
                    'upload_time': datetime.datetime(2012, 2, 2, 11, 32, 00),
                    'url': 'http://pypi.python.org/packages/source/r/'
                        'localshop/localshop-0.1.tar.gz'
                }]

            package = get_package_urls('Localshop')

            client.search.called_with({'name': 'Localshop'})

        package = models.Package.objects.get(pk=package.pk)
        self.assertEqual(package.releases.count(), 1)
