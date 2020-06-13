from __future__ import unicode_literals

import pytest
from django.urls import reverse

from localshop.apps.packages.tasks import fetch_package
from tests.factories import ReleaseFileFactory


@pytest.mark.django_db
def test_success(django_app, admin_user, repository, pypi_stub):
    repository.upstream_pypi_url = pypi_stub
    repository.save()
    release_file = ReleaseFileFactory(release__package__repository=repository)

    response = django_app.get(
        reverse('packages:simple_detail', kwargs={
            'slug': release_file.release.package.normalized_name,
            'repo': release_file.release.package.repository.slug
        }), user=admin_user)

    assert response.status_code == 200
    assert 'Links for Test_Package' in response.unicode_body

    a_elms = response.html.select('a')
    assert len(a_elms) == 1
    assert a_elms[0]['href'] == (
        'http://testserver/repo/default/download/Test_Package/1/' +
        'test-1.0.0-sdist.zip#md5=62ecd3ee980023db87945470aa2b347b')
    assert a_elms[0]['rel'][0] == 'package'


@pytest.mark.django_db
def test_success_redirect_to_normalized_name(django_app, admin_user, repository, pypi_stub):
    repository.upstream_pypi_url = pypi_stub
    repository.save()
    release_file = ReleaseFileFactory(release__package__repository=repository)

    response = django_app.get(
        reverse('packages:simple_detail', kwargs={
            'slug': release_file.release.package.name,
            'repo': release_file.release.package.repository.slug
        }), user=admin_user)

    assert response.status_code == 302
    assert response.headers['Location'] == '/repo/%s/%s/' % (
        repository.slug, release_file.release.package.normalized_name)


@pytest.mark.django_db
def test_missing_package_local_package(django_app, admin_user, repository,
                                       pypi_stub):
    repository.upstream_pypi_url = pypi_stub
    repository.save()

    fetch_package.run(repository.pk, 'minibar')

    response = django_app.get(
        reverse('packages:simple_detail', kwargs={
            'slug': 'minibar',
            'repo': repository.slug,
        }), user=admin_user)

    assert response.status_code == 200
    assert 'Links for minibar' in response.unicode_body
    assert 'minibar-0.4.0-py2.py3-none-any.whl#md5=0bbdf41e028a4e6c75dfbd59660b6328' in response.unicode_body
    assert 'minibar-0.4.0.tar.gz#md5=a3768a7f948871d8e47b146053265100' in response.unicode_body
    assert 'minibar-0.1.tar.gz#md5=c935bfa49cb49e4f97fb8e24371105d7' in response.unicode_body


@pytest.mark.django_db
def test_nonexistent_package(django_app, admin_user, repository, pypi_stub):
    repository.upstream_pypi_url = pypi_stub
    repository.save()

    response = django_app.get(
        reverse('packages:simple_detail', kwargs={
            'slug': 'nonexistent',
            'repo': repository.slug,
        }), user=admin_user)

    assert response.url == '%s/nonexistent' % pypi_stub
    assert response.status_code == 302


@pytest.mark.django_db
def test_wrong_package_name_case(django_app, admin_user, repository, pypi_stub):
    repository.upstream_pypi_url = pypi_stub
    repository.save()

    ReleaseFileFactory(
        release__package__repository=repository,
        release__package__name='minibar',
        release__package__normalized_name='minibar')

    response = django_app.get(
        reverse('packages:simple_detail', kwargs={
            'slug': 'Minibar',
            'repo': 'default'
        }), user=admin_user)

    assert response.status_code == 302
    assert response.url == '/repo/default/minibar/'
