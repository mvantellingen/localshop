import pytest

from django.core.urlresolvers import reverse

from localshop.apps.permissions.models import CIDR
from tests.apps.packages.factories import ReleaseFileFactory
from localshop.apps.packages.tasks import fetch_package


@pytest.mark.django_db
def test_success(client, admin_user, pypi_stub):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    release_file = ReleaseFileFactory()

    response = client.get(reverse('packages-simple:simple_detail',
                                  kwargs={'slug': release_file.release.package.name}))

    assert response.status_code == 200
    assert 'Links for test-package' in response.content
    assert ('<a href="/packages/test-package/download/1/test-1.0.0-sdist.zip'
            '#md5=62ecd3ee980023db87945470aa2b347b" rel="package">'
            'test-1.0.0-sdist.zip</a>') in response.content


@pytest.mark.django_db
def test_missing_package_local_package(client, admin_user, pypi_stub):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    fetch_package.run('minibar')

    response = client.get(reverse('packages-simple:simple_detail',
                                  kwargs={'slug': 'minibar'}))

    assert response.status_code == 200
    assert 'Links for minibar' in response.content
    assert 'minibar-0.4.0-py2.py3-none-any.whl#md5=0bbdf41e028a4e6c75dfbd59660b6328' in response.content
    assert 'minibar-0.4.0.tar.gz#md5=a3768a7f948871d8e47b146053265100' in response.content
    assert 'minibar-0.1.tar.gz#md5=c935bfa49cb49e4f97fb8e24371105d7' in response.content


@pytest.mark.django_db
def test_nonexistent_package(client, admin_user, pypi_stub):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    response = client.get(reverse('packages-simple:simple_detail',
                                  kwargs={'slug': 'nonexistent'}))

    assert response.url == 'https://pypi.python.org/simple/nonexistent'
    assert response.status_code == 302


@pytest.mark.django_db
def test_wrong_package_name_case(client, admin_user, pypi_stub):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    ReleaseFileFactory(release__package__name='minibar')

    response = client.get(reverse('packages-simple:simple_detail',
                                  kwargs={'slug': 'Minibar'}))

    assert response.status_code == 302
    assert response.url == 'http://testserver/simple/minibar/'
