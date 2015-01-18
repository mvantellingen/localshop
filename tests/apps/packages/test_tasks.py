from md5 import md5

import mock
import pytest

from localshop.apps.packages import tasks, models
from tests.apps.packages.factories import ReleaseFileFactory


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_file(requests_mock):
    file_data = 'My cool package'
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

    release_file = models.ReleaseFile.objects.get(pk=release_file.pk)

    assert release_file.distribution.read() == file_data
    assert release_file.distribution.name == '2.7/t/test-package/test-1.0.0-sdist.zip'


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_file_incorrect_md5_sum(requests_mock):
    file_data = 'My cool package'
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
