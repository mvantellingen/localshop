from __future__ import unicode_literals

from base64 import standard_b64encode

import pytest
from django.utils import six

from localshop.apps.packages.models import Package

from tests.factories import ReleaseFileFactory
from tests.utils import NamedStringIO


def basic_auth_header(username, password):
    auth_str = b':'.join((username.encode('utf-8'), password.encode('utf-8')))

    string = 'Basic %s' % standard_b64encode(auth_str).decode('utf-8')
    return tostr(string)


def tostr(value):
    return str(value)


REGISTER_POST = '\n'.join([
    '',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name="license"',
    '',
    'BSD',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name="name"',
    '',
    'localshop',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name="metadata_version"',
    '',
    '1.0',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name="author"',
    '',
    'Michael van Tellingen',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name="home_page"',
    '',
    'http://github.com/mvantellingen/localshop',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name=":action"',
    '',
    'submit',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name="download_url"',
    '',
    'UNKNOWN',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name="summary"',
    '',
    'A private pypi server including auto-mirroring of pypi.',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name="author_email"',
    '',
    'michaelvantellingen@gmail.com',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name="version"',
    '',
    '0.1',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name="platform"',
    '',
    'UNKNOWN',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    'Content-Disposition: form-data; name="description"',
    '',
    'UNKNOWN',
    '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254--',
    ''])


@pytest.mark.parametrize('separator', ['\n', '\r\n'])
def test_package_upload(app, admin_user, repository, separator):
    post_data = separator.join([
        '',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="comment"',
        '',
        '',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="metadata_version"',
        '',
        '1.0',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="filetype"',
        '',
        'sdist',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="protcol_version"',
        '',
        '1',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="author"',
        '',
        'Michael van Tellingen',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="home_page"',
        '',
        'http://github.com/mvantellingen/localshop',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="download_url"',
        '',
        'UNKNOWN',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="content";filename="tmpf3bcEV"',
        '',
        'binary-test-data-here',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="platform"',
        '',
        'UNKNOWN',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="version"',
        '',
        '0.1',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="description"',
        '',
        'UNKNOWN',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="md5_digest"',
        '',
        '06ffe94789d7bd9efba1109f40e935cf',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name=":action"',
        '',
        'file_upload',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="name"',
        '',
        'localshop',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="license"',
        '',
        'BSD',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="pyversion"',
        '',
        'source',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="summary"',
        '',
        'A private pypi server including auto-mirroring of pypi.',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Content-Disposition: form-data; name="author_email"',
        '',
        'michaelvantellingen@gmail.com',
        '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254--',
        ''])

    headers = {
        'Content-type': tostr('multipart/form-data; boundary=--------------GHSKFJDLGDS7543FJKLFHRE75642756743254'),
        'Authorization': basic_auth_header('admin', 'password'),
    }

    response = app.post(
        '/repo/%s/' % repository.slug, post_data, headers=headers, user=admin_user)

    assert response.status_code == 200

    package = Package.objects.filter(name='localshop').first()

    assert package is not None
    assert package.is_local is True
    assert package.releases.count() == 1

    release = package.releases.first()

    assert release.author == 'Michael van Tellingen'
    assert release.author_email == 'michaelvantellingen@gmail.com'
    assert release.description == ''
    assert release.download_url == ''
    assert release.home_page == 'http://github.com/mvantellingen/localshop'
    assert release.license == 'BSD'
    assert release.metadata_version == '1.0'
    assert release.summary == 'A private pypi server including auto-mirroring of pypi.'
    assert release.version == '0.1'
    assert release.files.count() == 1

    release_file = release.files.first()

    assert release_file is not None
    assert release_file.python_version == 'source'
    assert release_file.filetype == 'sdist'
    assert release_file.md5_digest == '06ffe94789d7bd9efba1109f40e935cf'
    assert release_file.distribution.read() == six.b('binary-test-data-here')


def test_package_register(app, repository, admin_user):
    headers = {
        'Content-type': tostr('multipart/form-data; boundary=--------------GHSKFJDLGDS7543FJKLFHRE75642756743254'),
        'Authorization': basic_auth_header('admin', 'password'),
    }

    response = app.post(
        '/repo/%s/' % repository.slug, REGISTER_POST, headers=headers)

    assert response.status_code == 200

    package = repository.packages.filter(name='localshop').first()

    assert package is not None
    assert package.is_local is True
    assert package.releases.count() == 1

    release = package.releases.first()

    assert release.author == 'Michael van Tellingen'
    assert release.author_email == 'michaelvantellingen@gmail.com'
    assert release.description == ''
    assert release.download_url == ''
    assert release.home_page == 'http://github.com/mvantellingen/localshop'
    assert release.license == 'BSD'
    assert release.metadata_version == '1.0'
    assert release.summary == 'A private pypi server including auto-mirroring of pypi.'
    assert release.version == '0.1'


def test_missing_auth(app, repository, admin_user):
    headers = {
        'Content-type': tostr('multipart/form-data; boundary=--------------GHSKFJDLGDS7543FJKLFHRE75642756743254'),
    }

    app.post(
        '/repo/%s/' % repository.slug, REGISTER_POST, headers=headers,
        status=401)


def test_invalid_auth(app, repository, admin_user):
    headers = {
        'Content-type': tostr('multipart/form-data; boundary=--------------GHSKFJDLGDS7543FJKLFHRE75642756743254'),
        'Authorization': basic_auth_header('admin', 'invalid'),
    }

    app.post(
        '/repo/%s/' % repository.slug, REGISTER_POST, headers=headers,
        status=401)


def test_invalid_action(app, repository, admin_user):
    headers = {
        'Authorization': basic_auth_header('admin', 'password'),
    }

    data = {
        ':action': 'invalid',
        'name': 'test',
        'version': '1.0',
    }

    response = app.post(
        '/repo/%s/' % repository.slug, params=data,
        upload_files=[('content', 'file.tgz', b'Hi')],
        headers=headers, status=404)

    assert response.unicode_body == 'Unknown action: invalid'


def test_missing_name(app, repository, admin_user):
    headers = {
        'Authorization': basic_auth_header('admin', 'password'),
    }

    data = {
        ':action': 'file_upload',
        'version': '1.0',
    }

    response = app.post(
        '/repo/%s/' % repository.slug, params=data,
        upload_files=[('content', 'file.tgz', b'Hi')],
        headers=headers, status=400)

    assert response.unicode_body == 'No name or version given'


def test_missing_version(app, repository, admin_user):
    headers = {
        'Authorization': basic_auth_header('admin', 'password'),
    }

    data = {
        ':action': 'file_upload',
        'name': 'test',
    }

    response = app.post(
        '/repo/%s/' % repository.slug, params=data,
        upload_files=[('content', 'file.tgz', b'Hi')],
        headers=headers, status=400)

    assert response.unicode_body == 'No name or version given'


def test_upload_should_not_overwrite_pypi_package(app, repository, admin_user):
    ReleaseFileFactory(
        release__package__repository=repository,
        release__package__name='localshop')

    headers = {
        'Content-type': tostr('multipart/form-data; boundary=--------------GHSKFJDLGDS7543FJKLFHRE75642756743254'),
        'Authorization': basic_auth_header('admin', 'password'),
    }

    response = app.post(
        '/repo/%s/' % repository.slug, REGISTER_POST, headers=headers,
        status=400)

    assert response.unicode_body == 'localshop is a pypi package!'


def test_package_name_with_whitespace(app, repository, admin_user):
    headers = {
        'Authorization': basic_auth_header('admin', 'password'),
    }

    data = {
        ':action': 'file_upload',
        'version': '1.0',
        'metadata_version': '1.0',
        'filetype': 'sdist',
        'md5_digest': '06ffe94789d7bd9efba1109f40e935cf',
    }
    data["name"] = "invalid name"

    response = app.post(
        '/repo/%s/' % repository.slug, params=data,
        upload_files=[('content', 'file.tgz', b'Hi')],
        headers=headers, status=400)

    assert response.status == (
        '400 Enter a valid name consisting of letters, numbers, underscores or hyphens')


def test_package_name_with_hyphen_instead_underscore(app, repository,
                                                     admin_user):
    headers = {
        'Authorization': basic_auth_header('admin', 'password'),
    }

    data = {
        ':action': 'file_upload',
        'name': 'package-name',
        'version': '1.0',
        'metadata_version': '1.0',
        'filetype': 'sdist',
        'md5_digest': '06ffe94789d7bd9efba1109f40e935cf',
    }

    response = app.post(
        '/repo/%s/' % repository.slug, params=data,
        upload_files=[('content', 'file.tgz', b'Hi')],
        headers=headers)

    assert response.status_code == 200

    data['name'] = 'package_name'
    data['version'] = '2.0'
    response = app.post(
        '/repo/%s/' % repository.slug, params=data,
        upload_files=[('content', 'file.tgz', b'Hi')],
        headers=headers)

    assert response.status_code == 200

    assert Package.objects.count() == 1
    package = Package.objects.first()
    assert package.name == 'package-name'
    assert package.releases.count() == 2
    assert package.releases.filter(version='2.0').exists()
    assert package.releases.filter(version='1.0').exists()


@pytest.mark.django_db
def test_invalid_version_upload(client, settings, repository, admin_user):
    settings.LOCALSHOP_VERSIONING_TYPE = 'versio.version_scheme.Simple3VersionScheme'

    auth = {
        'HTTP_AUTHORIZATION': basic_auth_header('admin', 'password'),
    }

    data = {
        ':action': 'file_upload',
        'name': 'package-name',
        'version': '01.0',
        'metadata_version': '1.0',
        'md5_digest': '06ffe94789d7bd9efba1109f40e935cf',
        'filetype': 'sdist',
        'content': NamedStringIO(b'Hi', name='blabla'),
    }

    response = client.post(
        '/repo/%s/' % repository.slug, data=data, **auth)

    assert response.status_code == 400
    assert "Invalid version supplied '01.0' for 'versio.version_scheme.Simple3VersionScheme' scheme." == response.reason_phrase


@pytest.mark.django_db
def test_valid_version_upload(client, settings, repository, admin_user):
    """Test a valid version upload when enforcement is activated"""
    settings.LOCALSHOP_VERSIONING_TYPE = 'versio.version_scheme.Simple3VersionScheme'

    auth = {
        'HTTP_AUTHORIZATION': basic_auth_header('admin', 'password'),
    }

    data = {
        ':action': 'file_upload',
        'name': 'package-name',
        'version': '0.1.0',
        'metadata_version': '1.0',
        'md5_digest': '06ffe94789d7bd9efba1109f40e935cf',
        'filetype': 'sdist',
        'content': NamedStringIO(b'Hi', name='blabla'),
    }

    response = client.post(
        '/repo/%s/' % repository.slug, data=data, **auth)

    assert response.status_code == 200
