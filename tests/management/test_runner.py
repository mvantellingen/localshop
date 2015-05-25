import copy
import os
import imp

import mock

from whitenoise.django import DjangoWhiteNoise
from django.test import TestCase

from localshop.runner import main
from localshop import wsgi

manage_instance = mock.MagicMock()
manage_mock = mock.MagicMock(return_value=manage_instance)


class TestWSGI(TestCase):
    def test_init_wsgi_application(self):
        self.assertIsInstance(wsgi.application, DjangoWhiteNoise)

    def test_set_env_defaults(self):
        # backup and remove global environment vars
        oldenv = copy.copy(os.environ)
        del os.environ['DJANGO_SETTINGS_MODULE']
        del os.environ['DJANGO_CONFIGURATION']
        imp.reload(wsgi)
        self.assertIn('DJANGO_SETTINGS_MODULE', os.environ)
        self.assertIn('DJANGO_CONFIGURATION', os.environ)
        self.assertEqual(os.environ['DJANGO_SETTINGS_MODULE'],
                         'localshop.settings')
        self.assertEqual(os.environ['DJANGO_CONFIGURATION'], 'Localshop')
        os.environ = oldenv


@mock.patch('django.core.management.ManagementUtility', manage_mock)
class TestRunner(TestCase):
    def tearDown(self):
        manage_instance.reset_mock()
        manage_mock.reset_mock()

    @mock.patch('sys.argv', [])
    def test_no_args_passed_manager(self):
        main()
        manage_mock.assert_called_once_with([])
        manage_instance.execute.assert_called_once_with()

    @mock.patch('sys.argv', ['init', '--no-superuser'])
    def test_args_passed_manager(self):
        main()
        manage_mock.assert_called_once_with(['init', '--no-superuser'])
        manage_instance.execute.assert_called_once_with()

    def test_set_env_defaults(self):
        # backup and remove global environment vars
        oldenv = copy.copy(os.environ)
        del os.environ['DJANGO_SETTINGS_MODULE']
        del os.environ['DJANGO_CONFIGURATION']
        main()
        self.assertIn('DJANGO_SETTINGS_MODULE', os.environ)
        self.assertIn('DJANGO_CONFIGURATION', os.environ)
        self.assertEqual(os.environ['DJANGO_SETTINGS_MODULE'],
                         'localshop.settings')
        self.assertEqual(os.environ['DJANGO_CONFIGURATION'], 'Localshop')
        os.environ = oldenv
