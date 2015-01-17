from md5 import md5

from django.core.urlresolvers import reverse
from mock import Mock
import mock
import pytest

from localshop.apps.packages.views import download_file
from localshop.apps.permissions.models import CIDR

from tests.apps.packages.factories import ReleaseFileFactory


@mock.patch('localshop.apps.packages.tasks.download_file')
@pytest.mark.django_db
def test_download_pypi_release(download_file_mock, rf):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    release_file = ReleaseFileFactory(distribution=None)

    args = (release_file.release.package.name,
            release_file.pk,
            release_file.filename)

    request = rf.get(reverse('packages:download', args=args))

    response = download_file(request, *args)

    # The request is redirected to PyPI
    assert response.status_code == 302
    assert response.url == release_file.url

    # The download file task must the queued
    assert download_file_mock.delay.call_count == 1
    assert download_file_mock.delay.call_args[1] == {'pk': release_file.pk}


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_pypi_release_when_isolated_is_on(requests_mock, rf, settings):
    file_data = 'Hello from PyPI'
    md5_digest = md5(file_data).hexdigest()

    settings.LOCALSHOP_ISOLATED = True

    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    release_file = ReleaseFileFactory(distribution=None, md5_digest=md5_digest)

    args = (release_file.release.package.name,
            release_file.pk,
            release_file.filename)

    requests_mock.return_value = Mock(**{
            'headers': {
                'content-length': len(file_data),
                'content-type': 'application/octet-stream',
            },
            'content': file_data,
        })

    request = rf.get(reverse('packages:download', args=args))
    response = download_file(request, *args)

    assert response.status_code == 200
    assert response.content == file_data
    requests_mock.assert_called_with(
        u'http://www.example.org/download/test-1.0.0-sdist.zip',
        proxies=None, stream=True)


@pytest.mark.parametrize('isolated', [True, False])
@pytest.mark.django_db
def test_download_local_release(rf, isolated, settings):
    settings.LOCALSHOP_ISOLATED = isolated

    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    release_file = ReleaseFileFactory()

    args = (release_file.release.package.name,
            release_file.pk,
            release_file.filename)

    request = rf.get(reverse('packages:download', args=args))

    response = download_file(request, *args)

    # Localshop must return the release file
    assert response.status_code == 200
    assert response.content == 'the file data'
    assert response.get('Content-Length') == '13'
    assert response.get('Content-Disposition') == 'attachment; filename=test-1.0.0-sdist.zip'
