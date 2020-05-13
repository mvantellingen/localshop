import os
from hashlib import md5

import mock
import pytest
from django.urls import reverse
from django.utils import six
from mock import Mock

from localshop.apps.packages import views
from tests.factories import ReleaseFileFactory


@mock.patch('localshop.apps.packages.tasks.download_file')
@pytest.mark.django_db
def test_download_pypi_release(download_file_mock, repository, rf):
    release_file = ReleaseFileFactory(
        release__package__repository=repository, distribution=None)

    url_kwargs = {
        'repo': repository.slug,
        'name': release_file.release.package.name,
        'pk': release_file.pk,
        'filename': release_file.filename
    }
    request = rf.get(reverse('packages:download', kwargs=url_kwargs))
    response = views.DownloadReleaseFile.as_view()(request, **url_kwargs)

    # The request is redirected to PyPI
    assert response.status_code == 302
    assert response.url == release_file.url

    # The download file task must the queued
    assert download_file_mock.delay.call_count == 1
    assert download_file_mock.delay.call_args[1] == {'pk': release_file.pk}


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_pypi_release_when_isolated_is_on(requests_mock, rf,
                                                   repository, settings):
    file_data = six.b('Hello from PyPI')
    md5_digest = md5(file_data).hexdigest()

    settings.LOCALSHOP_ISOLATED = True

    release_file = ReleaseFileFactory(
        release__package__repository=repository,
        distribution=None, md5_digest=md5_digest)

    url_kwargs = {
        'repo': repository.slug,
        'name': release_file.release.package.name,
        'pk': release_file.pk,
        'filename': release_file.filename
    }

    requests_mock.return_value = Mock(**{
        'headers': {
            'content-length': len(file_data),
            'content-type': 'application/octet-stream',
        },
        'content': file_data,
    })

    request = rf.get(reverse('packages:download', kwargs=url_kwargs))
    response = views.DownloadReleaseFile.as_view()(request, **url_kwargs)

    assert response.status_code == 200
    assert response.content == file_data
    requests_mock.assert_called_with(
        u'http://www.example.org/download/test-1.0.0-sdist.zip',
        proxies=None, stream=True)


@pytest.mark.parametrize('isolated', [True, False])
@pytest.mark.django_db
def test_download_local_release(rf, isolated, repository, settings):
    settings.LOCALSHOP_ISOLATED = isolated

    release_file = ReleaseFileFactory(
        release__package__repository=repository)

    url_kwargs = {
        'repo': repository.slug,
        'name': release_file.release.package.name,
        'pk': release_file.pk,
        'filename': release_file.filename
    }

    request = rf.get(reverse('packages:download', kwargs=url_kwargs))
    response = views.DownloadReleaseFile.as_view()(request, **url_kwargs)

    # Localshop must return the release file
    assert response.status_code == 200
    assert response.content == six.b('the file data')
    assert response.get('Content-Length') == '13'
    assert response.get('Content-Disposition') == 'attachment; filename=test-1.0.0-sdist.zip'


@mock.patch('localshop.apps.packages.tasks.download_file')
@pytest.mark.django_db
def test_release_with_a_missing_file(download_file_mock, repository, rf):
    """
    If a local ReleaseFile had a missing file we must set local as False,
    redirect to the PyPI, requeue the download_file task.
    """
    release_file = ReleaseFileFactory(
        release__package__repository=repository)
    os.remove(release_file.distribution.path)

    url_kwargs = {
        'repo': repository.slug,
        'name': release_file.release.package.name,
        'pk': release_file.pk,
        'filename': release_file.filename
    }

    request = rf.get(reverse('packages:download', kwargs=url_kwargs))
    response = views.DownloadReleaseFile.as_view()(request, **url_kwargs)

    # The request is redirected to PyPI
    assert response.status_code == 302
    assert response.url == release_file.url

    # The download file task must the queued
    assert download_file_mock.delay.call_count == 1
    assert download_file_mock.delay.call_args[1] == {'pk': release_file.pk}
