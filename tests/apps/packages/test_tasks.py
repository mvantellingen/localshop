from hashlib import md5

import mock
import pytest
from django.utils import six

from localshop.apps.packages import models, tasks
from tests.factories import PackageFactory, ReleaseFileFactory


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_file(requests_mock, tmpdir, settings):
    settings.MEDIA_ROOT = tmpdir
    file_data = six.b('My cool package')
    release_file = ReleaseFileFactory(
        distribution=None,
        md5_digest=md5(file_data).hexdigest())

    requests_mock.return_value = mock.Mock(**{
            'headers': {
                'content-length': len(file_data),
                'content-type': 'application/octet-stream',
            },
            'content': file_data,
        })

    tasks.download_file.run(release_file.pk)

    release_file = models.ReleaseFile.objects.get(pk=release_file.pk)

    assert release_file.distribution.read() == file_data
    assert release_file.distribution.size == len(file_data)
    assert release_file.distribution.name == (
        'default/2.7/T/Test_Package/test-1.0.0-sdist.zip')


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_file_incorrect_md5_sum(requests_mock):
    file_data = six.b('My cool package')
    release_file = ReleaseFileFactory(distribution=None, md5_digest='arcoiro')

    requests_mock.return_value = mock.Mock(**{
            'headers': {
                'content-length': len(file_data),
                'content-type': 'application/octet-stream',
            },
            'content': file_data,
        })

    tasks.download_file.run(release_file.pk)

    release_file = models.ReleaseFile.objects.get(pk=release_file.pk)

    assert not release_file.distribution


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_file_missing_content_length(requests_mock, settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir
    file_data = six.b('My cool package')
    release_file = ReleaseFileFactory(distribution=None,
                                      md5_digest=md5(file_data).hexdigest())

    requests_mock.return_value = mock.Mock(**{
            'headers': {
                'content-type': 'application/octet-stream',
            },
            'content': file_data,
        })

    tasks.download_file.run(release_file.pk)

    release_file = models.ReleaseFile.objects.get(pk=release_file.pk)

    assert release_file.distribution.read() == file_data
    assert release_file.distribution.size == len(file_data)
    assert release_file.distribution.name == (
        'default/2.7/T/Test_Package/test-1.0.0-sdist.zip')


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_file_with_proxy_enabled(requests_mock, settings):
    settings.LOCALSHOP_HTTP_PROXY = {
        "http": "http://10.10.1.10:3128/",
    }
    file_data = six.b('My cool package')
    release_file = ReleaseFileFactory(distribution=None,
                                      md5_digest=md5(file_data).hexdigest())

    requests_mock.return_value = mock.Mock(**{
            'headers': {
                'content-length': len(file_data),
                'content-type': 'application/octet-stream',
            },
            'content': file_data,
        })

    tasks.download_file.run(release_file.pk)

    requests_mock.assert_called_once_with(
        'http://www.example.org/download/test-1.0.0-sdist.zip',
        proxies=settings.LOCALSHOP_HTTP_PROXY,
        stream=True)


@mock.patch('localshop.apps.packages.tasks.fetch_package')
@pytest.mark.django_db
def test_update_package_should_call_get_package_data(fetch_pkg_mock):
    PackageFactory(name='local', normalized_name='local', is_local=True)
    pypi_package = PackageFactory(name='pypi', normalized_name='pypi', is_local=False)

    tasks.refresh_repository_mirrors()

    assert fetch_pkg_mock.call_count == 1
    fetch_pkg_mock.assert_called_once_with(pypi_package.repository.pk, pypi_package.name)
