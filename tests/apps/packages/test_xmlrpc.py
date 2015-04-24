import pytest
import xmlrpclib

from localshop.apps.permissions.models import CIDR
from tests.apps.packages.factories import ReleaseFactory


@pytest.mark.django_db
def test_search_package_name(client, admin_user, live_server):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    ReleaseFactory(package__name='my-package',
                   summary='Test summary')

    client = xmlrpclib.ServerProxy(live_server + '/RPC2')
    response = client.search({'name': 'my-package'})

    assert response == [{
        '_pypi_ordering': 0,
        'name': 'my-package',
        'summary': 'Test summary',
        'version': '1.0.0'}]


@pytest.mark.django_db
def test_search_package_summary(client, admin_user, live_server):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    ReleaseFactory(package__name='my-package',
                   summary='Test summary')

    client = xmlrpclib.ServerProxy(live_server + '/RPC2')
    response = client.search({'summary': ['Test summary']})

    assert response == [{
        '_pypi_ordering': 0,
        'name': 'my-package',
        'summary': 'Test summary',
        'version': '1.0.0'}]


@pytest.mark.django_db
def test_search_operator_and(client, admin_user, live_server):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    ReleaseFactory(package__name='my-package-1',
                   summary='Test summary')

    ReleaseFactory(package__name='arcoiro',
                   summary='Test summary')

    ReleaseFactory(package__name='my-package-2',
                   summary='arcoiro')

    client = xmlrpclib.ServerProxy(live_server + '/RPC2')
    response = client.search({'name': ['my-package'],
                              'summary': ['Test summary']}, 'and')

    assert response == [{
        '_pypi_ordering': 0,
        'name': 'my-package-1',
        'summary': 'Test summary',
        'version': '1.0.0'}]


@pytest.mark.django_db
def test_search_operator_or(client, admin_user, live_server):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    ReleaseFactory(package__name='my-package-1',
                   summary='Test summary')

    ReleaseFactory(package__name='arcoiro',
                   summary='Test summary')

    ReleaseFactory(package__name='my-package-2',
                   summary='arcoiro')

    client = xmlrpclib.ServerProxy(live_server + '/RPC2')
    response = client.search({'name': ['my-package'],
                              'summary': ['Test summary']}, 'or')

    assert response == [{
            '_pypi_ordering': 0,
            'name': 'arcoiro',
            'summary': 'Test summary',
            'version': '1.0.0'
        },
        {
            '_pypi_ordering': 0,
            'name': 'my-package-1',
            'summary': 'Test summary',
            'version': '1.0.0'
        },
        {
            '_pypi_ordering': 0,
            'name': 'my-package-2',
            'summary': 'arcoiro',
            'version': '1.0.0'
        }]


@pytest.mark.django_db
def test_search_invalid_fields_are_ignores(client, admin_user, live_server):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    ReleaseFactory(package__name='my-package',
                   summary='Test summary')

    client = xmlrpclib.ServerProxy(live_server + '/RPC2')
    response = client.search({'name': ['my-package'], 'invalid': ['Ops']})

    assert response == [{
        '_pypi_ordering': 0,
        'name': 'my-package',
        'summary': 'Test summary',
        'version': '1.0.0'}]
