from django.test import TestCase
from localshop.packages import utils


class UtilsTest(TestCase):
    def test_get_package_urls(self):
        package = utils.get_package_urls('pip')

