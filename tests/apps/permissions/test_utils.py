from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from localshop.apps.permissions.utils import credentials_required
from localshop.apps.permissions import models


@credentials_required
def myview(request):
    return HttpResponse('ok')


class ProxiedIPText(TestCase):
    def setUp(self):
        models.CIDR.objects.create(cidr='192.168.1.1', require_credentials=False)
        self.factory = RequestFactory()

    def test_disabled(self):
        # never look at X-Forwarded-For if the setting is disabled (default)
        req = self.factory.get('/', REMOTE_ADDR='192.168.1.1', HTTP_X_FORWARDED_FOR='10.1.1.1')
        resp = myview(req)
        self.assertEqual(resp.status_code, 200)

        req = self.factory.get('/', REMOTE_ADDR='127.0.0.1', HTTP_X_FORWARDED_FOR='192.168.1.1')
        resp = myview(req)
        self.assertEqual(resp.status_code, 403)

        req = self.factory.get('/', REMOTE_ADDR='10.1.1.1', HTTP_X_FORWARDED_FOR='192.168.1.1')
        resp = myview(req)
        self.assertEqual(resp.status_code, 403)

    def test_proxied(self):
        with override_settings(LOCALSHOP_USE_PROXIED_IP=True):
            req = self.factory.get('/', REMOTE_ADDR='127.0.0.1', HTTP_X_FORWARDED_FOR='192.168.1.1')
            resp = myview(req)
            self.assertEqual(resp.status_code, 200)

            req = self.factory.get('/', REMOTE_ADDR='192.168.1.1', HTTP_X_FORWARDED_FOR='10.1.1.1')
            resp = myview(req)
            self.assertEqual(resp.status_code, 403)

    def test_proxied_last(self):
        # only the last hop counts (first in the list)
        with override_settings(LOCALSHOP_USE_PROXIED_IP=True):
            req = self.factory.get('/', REMOTE_ADDR='127.0.0.1', HTTP_X_FORWARDED_FOR='192.168.1.1, 10.1.1.1')
            resp = myview(req)
            self.assertEqual(resp.status_code, 200)

            req = self.factory.get('/', REMOTE_ADDR='127.0.0.1', HTTP_X_FORWARDED_FOR='10.1.1.1, 192.168.1.1')
            resp = myview(req)
            self.assertEqual(resp.status_code, 403)

    def test_proxied_mising(self):
        with override_settings(LOCALSHOP_USE_PROXIED_IP=True):
            req = self.factory.get('/', REMOTE_ADDR='127.0.0.1')
            resp = myview(req)
            self.assertEqual(resp.status_code, 403)

            # only uses the header, never falls back to REMOTE_ADDR
            req = self.factory.get('/', REMOTE_ADDR='192.168.1.1')
            resp = myview(req)
            self.assertEqual(resp.status_code, 403)
