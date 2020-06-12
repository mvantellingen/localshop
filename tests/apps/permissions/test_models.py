from django.test import TestCase

from localshop.apps.permissions import models
from tests.factories import CIDRFactory


class CidrTest(TestCase):
    def test_has_access(self):
        self.assertFalse(models.CIDR.objects.has_access('192.168.1.1'))

    def test_simple(self):
        cidr = CIDRFactory(cidr='192.168.1.1', require_credentials=True)
        assert cidr.repository.cidr_list.has_access('192.168.1.1')

    def test_cidr(self):
        cidr = CIDRFactory(cidr='192.168.1.0/24', require_credentials=True)
        assert cidr.repository.cidr_list.has_access('192.168.1.1')
