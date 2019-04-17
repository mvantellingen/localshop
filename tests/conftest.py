import os
import re

import pytest
import requests_mock
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore
from django.test.client import RequestFactory as BaseRequestFactory
from django.test.utils import override_settings

from localshop.packages.pypi import get_search_names
from tests.factories import CIDRFactory, RepositoryFactory


def pytest_configure(config):
    override = override_settings(
        ALLOWED_HOSTS=['*'],
        STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
        CELERY_TASK_ALWAYS_EAGER=True,
    )
    override.enable()


@pytest.fixture(scope='function')
def pypi_stub():
    with requests_mock.Mocker(real_http=True) as rm:
        wildcard_re = re.compile('^https://pypi\.internal/.*')
        rm.register_uri('GET', wildcard_re, status_code=404)

        pypi_dir = os.path.join(os.path.dirname(__file__), 'pypi_data')
        for filename in os.listdir(pypi_dir):
            with open(os.path.join(pypi_dir, filename), 'rb') as fh:
                content = fh.read()

            name, ext = os.path.splitext(filename)
            url = 'https://pypi.internal/pypi/%s/json' % name
            rm.register_uri('GET', url, content=content)

            # Register the alternative urls and redirect to original url
            for alt_name in get_search_names(name):
                if alt_name != name:
                    alt_url = 'https://pypi.internal/pypi/%s/json' % alt_name
                    rm.register_uri(
                        'GET',
                        alt_url,
                        headers={
                            'Location': url,
                        },
                        status_code=301)

        yield 'https://pypi.internal/pypi/'


@pytest.fixture(scope='function')
@pytest.mark.django_db
def repository(db):
    repo = RepositoryFactory()
    CIDRFactory(repository=repo)
    return repo


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
