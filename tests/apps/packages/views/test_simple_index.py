from base64 import standard_b64encode

from django.core.urlresolvers import reverse
import pytest
import requests

from localshop.apps.packages.models import Package
from localshop.apps.permissions.models import CIDR
from tests.apps.packages.factories import ReleaseFileFactory
from tests.utils import NamedStringIO


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
def test_package_upload(live_server, admin_user, separator):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

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
        'Content-type': 'multipart/form-data; boundary=--------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Authorization': 'Basic ' + standard_b64encode('admin:password')
    }

    response = requests.post(live_server + '/simple/', post_data, headers=headers)

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
    assert release.user == admin_user
    assert release.version == '0.1'
    assert release.files.count() == 1

    release_file = release.files.first()

    assert release_file is not None
    assert release_file.python_version == 'source'
    assert release_file.filetype == 'sdist'
    assert release_file.md5_digest == '06ffe94789d7bd9efba1109f40e935cf'
    assert release_file.distribution.read() == 'binary-test-data-here'


def test_package_register(live_server, admin_user):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    headers = {
        'Content-type': 'multipart/form-data; boundary=--------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Authorization': 'Basic ' + standard_b64encode('admin:password')
    }

    response = requests.post(live_server + '/simple/', REGISTER_POST, headers=headers)

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
    assert release.user == admin_user
    assert release.version == '0.1'


def test_missing_auth(live_server, admin_user):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    headers = {
        'Content-type': 'multipart/form-data; boundary=--------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
    }

    response = requests.post(live_server + '/simple/', REGISTER_POST, headers=headers)

    assert response.status_code == 401
    assert response.content == 'Missing auth header'


def test_invalid_auth(live_server, admin_user):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    headers = {
        'Content-type': 'multipart/form-data; boundary=--------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Authorization': 'Basic ' + standard_b64encode('moises:arcoiro')
    }

    response = requests.post(live_server + '/simple/', REGISTER_POST, headers=headers)

    assert response.status_code == 401
    assert response.content == 'Invalid username/password'


def test_invalid_action(live_server, admin_user):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    headers = {
        'Authorization': 'Basic ' + standard_b64encode('admin:password')
    }

    data = {
        ':action': 'invalid',
        'name': 'test',
        'version': '1.0',
    }

    response = requests.post(live_server + '/simple/', data=data, files={'content': 'Hi'}, headers=headers)

    assert response.status_code == 404
    assert response.content == 'Unknown action'


def test_missing_name(live_server, admin_user):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    headers = {
        'Authorization': 'Basic ' + standard_b64encode('admin:password')
    }

    data = {
        ':action': 'file_upload',
        'version': '1.0',
    }

    response = requests.post(live_server + '/simple/', data=data, files={'content': 'Hi'}, headers=headers)

    assert response.status_code == 400
    assert response.content == 'No name or version given'


def test_missing_version(live_server, admin_user):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    headers = {
        'Authorization': 'Basic ' + standard_b64encode('admin:password')
    }

    data = {
        ':action': 'file_upload',
        'name': 'test',
    }

    response = requests.post(live_server + '/simple/', data=data, files={'content': 'Hi'}, headers=headers)

    assert response.status_code == 400
    assert response.content == 'No name or version given'


def test_upload_should_not_overwrite_pypi_package(live_server, admin_user):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    ReleaseFileFactory(release__package__name='localshop')

    headers = {
        'Content-type': 'multipart/form-data; boundary=--------------GHSKFJDLGDS7543FJKLFHRE75642756743254',
        'Authorization': 'Basic ' + standard_b64encode('admin:password')
    }

    response = requests.post(live_server + '/simple/', REGISTER_POST, headers=headers)

    assert response.status_code == 400
    assert response.content == 'localshop is a pypi package!'


def test_package_name_with_hyphen_instead_underscore(live_server, admin_user):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    headers = {
        'Authorization': 'Basic ' + standard_b64encode('admin:password')
    }

    data = {
        ':action': 'file_upload',
        'name': 'package-name',
        'version': '1.0',
        'metadata_version': '1.0',
        'filetype': 'sdist',
        'md5_digest': '06ffe94789d7bd9efba1109f40e935cf',
    }

    response = requests.post(live_server + '/simple/', data=data, files={'content': 'Hi'}, headers=headers)

    assert response.status_code == 200

    data['name'] = 'package_name'
    data['version'] = '2.0'
    response = requests.post(live_server + '/simple/', data=data, files={'content': 'Hi'}, headers=headers)

    assert response.status_code == 200

    assert Package.objects.count() == 1
    package = Package.objects.first()
    assert package.name == 'package-name'
    assert package.releases.count() == 2
    assert package.releases.filter(version='2.0').exists()
    assert package.releases.filter(version='1.0').exists()


@pytest.mark.django_db
def test_invalid_version_upload(client, settings, admin_user):
    settings.LOCALSHOP_VERSIONING_TYPE = 'versio.version_scheme.Simple3VersionScheme'
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    auth = {
        'HTTP_AUTHORIZATION': 'Basic ' + standard_b64encode('admin:password')
    }

    data = {
        ':action': 'file_upload',
        'name': 'package-name',
        'version': '01.0',
        'metadata_version': '1.0',
        'md5_digest': '06ffe94789d7bd9efba1109f40e935cf',
        'filetype': 'sdist',
        'content': NamedStringIO(u'Hi', name='blabla')
    }

    response = client.post('/simple', data=data, **auth)

    assert response.status_code == 400
    assert "Invalid version supplied 01.0 for 'versio.version_scheme.Simple3VersionScheme' scheme" in response.content


@pytest.mark.django_db
def test_valid_version_upload(client, settings, admin_user):
    """Test a valid version upload when enforcement is activated"""

    settings.LOCALSHOP_VERSIONING_TYPE = 'versio.version_scheme.Simple3VersionScheme'
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    auth = {
        'HTTP_AUTHORIZATION': 'Basic ' + standard_b64encode('admin:password')
    }

    data = {
        ':action': 'file_upload',
        'name': 'package-name',
        'version': '0.1.0',
        'metadata_version': '1.0',
        'md5_digest': '06ffe94789d7bd9efba1109f40e935cf',
        'filetype': 'sdist',
        'content': NamedStringIO(u'Hi', name='blabla')
    }

    response = client.post('/simple', data=data, **auth)

    assert response.status_code == 200
