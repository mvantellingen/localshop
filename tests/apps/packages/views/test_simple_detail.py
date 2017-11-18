from __future__ import unicode_literals

import pytest
from django.core.urlresolvers import reverse

from localshop.apps.packages.tasks import fetch_package

from tests.factories import ReleaseFileFactory


@pytest.mark.django_db
def test_success(app, admin_user, repository, pypi_stub):
    repository.upstream_pypi_url = pypi_stub.url
    repository.save()
    release_file = ReleaseFileFactory(release__package__repository=repository)

    response = app.get(
        reverse('packages:simple_detail', kwargs={
            'slug': release_file.release.package.name,
            'repo': release_file.release.package.repository.slug
        }))

    assert response.status_code == 200
    assert 'Links for test-package' in response.unicode_body

    a_elms = response.html.select('a')
    assert len(a_elms) == 1
    assert a_elms[0]['href'] == (
        '/repo/default/download/test-package/1/test-1.0.0-sdist.zip' +
        '#md5=62ecd3ee980023db87945470aa2b347b')
    assert a_elms[0]['rel'][0] == 'package'


@pytest.mark.django_db
def test_missing_package_local_package(app, admin_user, repository,
                                       pypi_stub):
    repository.upstream_pypi_url = pypi_stub.url
    repository.save()

    fetch_package.run(repository.pk, 'minibar')

    response = app.get(
        reverse('packages:simple_detail', kwargs={
            'slug': 'minibar',
            'repo': repository.slug,
        }))

    assert response.status_code == 200
    assert 'Links for minibar' in response.unicode_body
    assert 'minibar-0.4.0-py2.py3-none-any.whl#md5=0bbdf41e028a4e6c75dfbd59660b6328' in response.unicode_body
    assert 'minibar-0.4.0.tar.gz#md5=a3768a7f948871d8e47b146053265100' in response.unicode_body
    assert 'minibar-0.1.tar.gz#md5=c935bfa49cb49e4f97fb8e24371105d7' in response.unicode_body


@pytest.mark.django_db
@pytest.mark.skip
def test_nonexistent_package(app, admin_user, repository, pypi_stub):
    repository.upstream_pypi_url = pypi_stub.url
    repository.save()

    response = app.get(
        reverse('packages:simple_detail', kwargs={
            'slug': 'nonexistent',
            'repo': repository.slug,
        }))

    assert response.url == '%s/nonexistent'  % pypi_stub.url
    assert response.status_code == 302


@pytest.mark.django_db
def test_wrong_package_name_case(app, admin_user, repository, pypi_stub):
    repository.upstream_pypi_url = pypi_stub.url
    repository.save()

    ReleaseFileFactory(
        release__package__repository=repository,
        release__package__name='minibar')

    response = app.get(
        reverse('packages:simple_detail', kwargs={
            'slug': 'Minibar',
            'repo': 'default'
        }))

    assert response.status_code == 302
    assert response.url == '/repo/default/minibar/'
