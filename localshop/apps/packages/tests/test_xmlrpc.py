from django.test import TestCase

from localshop.apps.packages import xmlrpc


class TestXMLRPC(TestCase):
    def test_search(self):
        rv = xmlrpc.search({'name': 'foo', 'summary': 'bar'}, 'or')
        self.assertEqual([], rv)
