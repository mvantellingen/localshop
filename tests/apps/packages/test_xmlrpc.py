import xmlrpc.client as xmlrpclib

import pytest

from tests.factories import ReleaseFactory


@pytest.fixture(params=['/RPC2', '/pypi'])
def rpc_endpoint(request):
    return request.param


@pytest.mark.django_db
def test_search_package_name(client, admin_user, live_server, repository,
                             rpc_endpoint):
    ReleaseFactory(
        package__name='my-package', package__repository=repository,
        summary='Test summary')

    client = xmlrpclib.ServerProxy(live_server + rpc_endpoint)
    response = client.search({'name': 'my-package'})

    assert response == [{
        '_pypi_ordering': 0,
        'name': 'my-package',
        'summary': 'Test summary',
        'version': '1.0.0'}]


@pytest.mark.django_db
def test_search_package_summary(client, admin_user, live_server, repository,
                                rpc_endpoint):
    ReleaseFactory(
        package__name='my-package', package__repository=repository,
        summary='Test summary')

    client = xmlrpclib.ServerProxy(live_server + rpc_endpoint)
    response = client.search({'summary': ['Test summary']})

    assert response == [{
        '_pypi_ordering': 0,
        'name': 'my-package',
        'summary': 'Test summary',
        'version': '1.0.0'}]


@pytest.mark.django_db
def test_search_operator_and(client, admin_user, live_server, repository,
                             rpc_endpoint):
    ReleaseFactory(package__name='my-package-1',
                   package__repository=repository,
                   summary='Test summary')

    ReleaseFactory(package__name='arcoiro',
                   package__repository=repository,
                   summary='Test summary')

    ReleaseFactory(package__name='my-package-2',
                   package__repository=repository,
                   summary='arcoiro')

    client = xmlrpclib.ServerProxy(live_server + rpc_endpoint)
    response = client.search({'name': ['my-package'],
                              'summary': ['Test summary']}, 'and')

    assert response == [{
        '_pypi_ordering': 0,
        'name': 'my-package-1',
        'summary': 'Test summary',
        'version': '1.0.0'}]


@pytest.mark.django_db
def test_search_operator_or(client, admin_user, live_server, repository,
                            rpc_endpoint):
    ReleaseFactory(package__name='my-package-1',
                   package__repository=repository,
                   summary='Test summary')

    ReleaseFactory(package__name='arcoiro',
                   package__repository=repository,
                   summary='Test summary')

    ReleaseFactory(package__name='my-package-2',
                   package__repository=repository,
                   summary='arcoiro')

    client = xmlrpclib.ServerProxy(live_server + rpc_endpoint)
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
def test_search_invalid_fields_are_ignores(client, admin_user, live_server,
                                           repository, rpc_endpoint):

    ReleaseFactory(package__name='my-package',
                   package__repository=repository,
                   summary='Test summary')

    client = xmlrpclib.ServerProxy(live_server + rpc_endpoint)
    response = client.search({'name': ['my-package'], 'invalid': ['Ops']})

    assert response == [{
        '_pypi_ordering': 0,
        'name': 'my-package',
        'summary': 'Test summary',
        'version': '1.0.0'}]
