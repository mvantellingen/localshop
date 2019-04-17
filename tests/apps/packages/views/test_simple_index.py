import uuid
from base64 import standard_b64encode

import pytest
from django.utils import six
from requests_toolbelt.multipart.encoder import MultipartEncoder

from localshop.packages.models import Package
from tests.factories import ReleaseFileFactory
from tests.utils import NamedStringIO


def basic_auth_header(username, password):
    username = str(username).encode('utf-8')
    password = str(password).encode('utf-8')
    auth_str = standard_b64encode(b':'.join((username, password)))
    return 'Basic %s' % auth_str.decode('utf-8')


@pytest.fixture
def register_post_data():
    return MultipartEncoder(fields={
        ':action': 'submit',
        'author_email': 'michaelvantellingen@gmail.com',
        'author': 'Michael van Tellingen',
        'description': 'UNKNOWN',
        'download_url': 'UNKNOWN',
        'home_page': 'http://github.com/mvantellingen/localshop',
        'license': 'BSD',
        'metadata_version': '1.0',
        'name': 'localshop',
        'platform': 'UNKNOWN',
        'summary': 'A private pypi server including auto-mirroring of pypi.',
        'version': '0.1',
    })


@pytest.fixture
def upload_post_data():
    return MultipartEncoder(fields={
        ':action': 'file_upload',

        'author_email': 'michaelvantellingen@gmail.com',
        'author': 'Michael van Tellingen',
        'description': 'UNKNOWN',
        'download_url': 'UNKNOWN',
        'home_page': 'http://github.com/mvantellingen/localshop',
        'license': 'BSD',
        'metadata_version': '1.0',
        'name': 'localshop',
        'platform': 'UNKNOWN',
        'summary': 'A private pypi server including auto-mirroring of pypi.',
        'version': '0.1',

        'comment': '',
        'protocol_version': '1',
        'content': ('tmpf3bcEV', 'binary-test-data-here'),
        'filetype': 'sdist',
        'md5_digest': '06ffe94789d7bd9efba1109f40e935cf',
        'pyversion': 'source',
    })


@pytest.mark.parametrize('separator', [b'\n', b'\r\n'])
def test_package_upload(django_app, admin_user, repository, upload_post_data,
                        separator):
    """Test package upload with \n and \r\n as separator.

    \r\n is actually the correct separator but there was a bug in older python
    versions which used \n. See http://bugs.python.org/issue10510
    """
    post_data = upload_post_data.to_string().replace(b'\r\n', separator)

    headers = {
        'Content-type': upload_post_data.content_type,
        'Authorization': basic_auth_header('admin', 'password'),
    }

    response = django_app.post(
        '/repo/%s/' % repository.slug,
        params=post_data,
        headers=headers,
        user=admin_user)

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


def test_package_register(django_app, repository, admin_user, register_post_data):
    key = admin_user.access_keys.create(comment='For testing')
    headers = {
        'Content-type': register_post_data.content_type,
        'Authorization': basic_auth_header(key.access_key, key.secret_key)
    }

    response = django_app.post(
        '/repo/%s/' % repository.slug,
        params=register_post_data.to_string(),
        headers=headers)

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


def test_missing_auth(django_app, repository, admin_user, register_post_data):
    headers = {
        'Content-type': register_post_data.content_type
    }

    django_app.post(
        '/repo/%s/' % repository.slug,
        params=register_post_data.to_string(),
        headers=headers,
        status=401)


def test_invalid_auth(django_app, repository, admin_user, register_post_data):
    access_key = uuid.uuid4()
    secret_key = uuid.uuid4()
    headers = {
        'Content-type': register_post_data.content_type,
        'Authorization': basic_auth_header(access_key, secret_key)
    }

    django_app.post(
        '/repo/%s/' % repository.slug,
        params=register_post_data.to_string(),
        headers=headers,
        status=401)


def test_invalid_auth_no_uuid(django_app, repository, admin_user, register_post_data):
    access_key = 'user'
    secret_key = 'password'
    headers = {
        'Content-type': register_post_data.content_type,
        'Authorization': basic_auth_header(access_key, secret_key)
    }

    django_app.post(
        '/repo/%s/' % repository.slug,
        params=register_post_data.to_string(),
        headers=headers,
        status=401)


def test_invalid_action(django_app, repository, admin_user):
    key = admin_user.access_keys.create(comment='For testing')
    headers = {
        'Authorization': basic_auth_header(key.access_key, key.secret_key)
    }

    data = {
        ':action': 'invalid',
        'name': 'test',
        'version': '1.0',
    }

    response = django_app.post(
        '/repo/%s/' % repository.slug, params=data,
        upload_files=[('content', 'file.tgz', b'Hi')],
        headers=headers, status=404)

    assert response.unicode_body == 'Unknown action: invalid'


def test_missing_name(django_app, repository, admin_user):
    key = admin_user.access_keys.create(comment='For testing')
    headers = {
        'Authorization': basic_auth_header(key.access_key, key.secret_key)
    }

    data = {
        ':action': 'file_upload',
        'version': '1.0',
    }

    response = django_app.post(
        '/repo/%s/' % repository.slug, params=data,
        upload_files=[('content', 'file.tgz', b'Hi')],
        headers=headers, status=400)

    assert response.unicode_body == 'No name or version given'


def test_missing_version(django_app, repository, admin_user):
    key = admin_user.access_keys.create(comment='For testing')
    headers = {
        'Authorization': basic_auth_header(key.access_key, key.secret_key)
    }

    data = {
        ':action': 'file_upload',
        'name': 'test',
    }

    response = django_app.post(
        '/repo/%s/' % repository.slug, params=data,
        upload_files=[('content', 'file.tgz', b'Hi')],
        headers=headers, status=400)

    assert response.unicode_body == 'No name or version given'


def test_upload_should_not_overwrite_pypi_package(
    django_app, repository, admin_user, upload_post_data
):
    ReleaseFileFactory(
        release__package__repository=repository,
        release__package__name='localshop')

    key = admin_user.access_keys.create(comment='For testing')
    headers = {
        'Content-type': upload_post_data.content_type,
        'Authorization': basic_auth_header(key.access_key, key.secret_key)
    }

    response = django_app.post(
        '/repo/%s/' % repository.slug,
        params=upload_post_data.to_string(),
        headers=headers,
        status=400)

    assert response.unicode_body == 'localshop is a pypi package!'


def test_package_name_with_whitespace(django_app, repository, admin_user):
    key = admin_user.access_keys.create(comment='For testing')
    headers = {
        'Authorization': basic_auth_header(key.access_key, key.secret_key)
    }

    data = {
        ':action': 'file_upload',
        'version': '1.0',
        'metadata_version': '1.0',
        'filetype': 'sdist',
        'md5_digest': '06ffe94789d7bd9efba1109f40e935cf',
    }
    data["name"] = "invalid name"

    response = django_app.post(
        '/repo/%s/' % repository.slug, params=data,
        upload_files=[('content', 'file.tgz', b'Hi')],
        headers=headers, status=400)

    assert response.status == (
        '400 Enter a valid name consisting of letters, numbers, underscores or hyphens')


def test_package_name_with_hyphen_instead_underscore(django_app, repository, admin_user):
    key = admin_user.access_keys.create(comment='For testing')
    headers = {
        'Authorization': basic_auth_header(key.access_key, key.secret_key)
    }

    data = {
        ':action': 'file_upload',
        'name': 'package-name',
        'version': '1.0',
        'metadata_version': '1.0',
        'filetype': 'sdist',
        'md5_digest': '06ffe94789d7bd9efba1109f40e935cf',
    }

    response = django_app.post(
        '/repo/%s/' % repository.slug, params=data,
        upload_files=[('content', 'file.tgz', b'Hi')],
        headers=headers)

    assert response.status_code == 200

    data['name'] = 'package_name'
    data['version'] = '2.0'
    response = django_app.post(
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

    key = admin_user.access_keys.create(comment='For testing')
    auth = {
        'HTTP_AUTHORIZATION': basic_auth_header(key.access_key, key.secret_key)
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
    assert response.reason_phrase == (
        "Invalid version supplied '01.0' for 'versio.version_scheme.Simple3VersionScheme' scheme.")


@pytest.mark.django_db
def test_valid_version_upload(client, settings, repository, admin_user):
    """Test a valid version upload when enforcement is activated"""
    settings.LOCALSHOP_VERSIONING_TYPE = 'versio.version_scheme.Simple3VersionScheme'

    key = admin_user.access_keys.create(comment='For testing')
    auth = {
        'HTTP_AUTHORIZATION': basic_auth_header(key.access_key, key.secret_key)
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
