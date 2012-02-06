from django.test import TestCase

from localshop.permissions import models


class CidrTest(TestCase):
    def test_has_access(self):
        self.assertFalse(models.CIDR.objects.has_access('192.168.1.1'))

    def test_simple(self):
        models.CIDR.objects.create(cidr='192.168.1.1')
        self.assertTrue(models.CIDR.objects.has_access('192.168.1.1'))

    def test_cidr(self):
        models.CIDR.objects.create(cidr='192.168.1.0/24')
        self.assertTrue(models.CIDR.objects.has_access('192.168.1.1'))
