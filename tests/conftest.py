import threading
from wsgiref.simple_server import make_server

import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore
from django.test.client import RequestFactory as BaseRequestFactory
from django_webtest import DjangoTestApp, WebTestMixin

from tests.factories import CIDRFactory, RepositoryFactory
from tests.utils import pypi_app


@pytest.yield_fixture(scope='session')
def pypi_stub():
    server = make_server('', 12946, pypi_app)  # Same port as LOCALSHOP_PYPI_URL

    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    yield server

    server.shutdown()


@pytest.fixture(scope='function')
@pytest.mark.django_db
def repository(db):
    repo = RepositoryFactory()
    CIDRFactory(repository=repo)
    return repo


@pytest.fixture(scope='function')
def app(request):
    """WebTest's TestApp.

    Patch and unpatch settings before and after each test.

    WebTestMixin, when used in a unittest.TestCase, automatically calls
    _patch_settings() and _unpatchsettings.

    from: https://gist.github.com/magopian/6673250

    """
    wtm = WebTestMixin()
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    return DjangoTestApp()


class RequestFactory(BaseRequestFactory):

    def request(self, user=None, **request):
        request = super(RequestFactory, self).request(**request)
        request.user = AnonymousUser()
        request.session = SessionStore()
        request._messages = FallbackStorage(request)
        return request


@pytest.fixture()
def rf():
    return RequestFactory()
