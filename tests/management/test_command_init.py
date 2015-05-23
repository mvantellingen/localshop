from copy import deepcopy
import os
import re

import mock

from django.test import TestCase, override_settings
from django.core import management

# from tests.apps.packages import factories

call_command_real = deepcopy(management.call_command)
TEST_HOME = os.path.join(os.path.dirname(__file__), 'home')
MOCK_ENV = {'LOCALSHOP_HOME': TEST_HOME}


class TestInitCommand(TestCase):
    def setUp(self):
        patch_call_command = mock.patch('django.core.management.call_command')
        patch_environ = mock.patch.dict('os.environ', MOCK_ENV)
        patch_mkdir = mock.patch('os.mkdir')
        patch_open = mock.patch('localshop.management.commands.init.open',
                                mock.mock_open(), create=True)

        self.mock_call = patch_call_command.start()
        self.mock_environ = patch_environ.start()
        self.mock_mkdir = patch_mkdir.start()
        self.mock_open = patch_open.start()

        self.addCleanup(patch_call_command.stop)
        self.addCleanup(patch_environ.stop)
        self.addCleanup(patch_mkdir.stop)
        self.addCleanup(patch_open.stop)

        self.assertNotEqual(self.mock_call, call_command_real)

    def test_commands_called(self):
        call_command_real('init')
        self.mock_call.assert_any_call(
            'syncdb', database='default',
            interactive=False)
        self.mock_call.assert_any_call(
            'migrate', database='default',
            interactive=False)
        self.mock_call.assert_any_call(
            'createsuperuser', database='default',
            interactive=True)

    def test_make_dir(self):
        call_command_real('init')
        self.mock_mkdir.assert_called_once_with(TEST_HOME)

    def test_config_file_contents(self):
        call_command_real('init')
        test_file = os.path.join(TEST_HOME, 'localshop.conf.py')
        self.mock_open.assert_called_once_with(test_file, 'w')
        fhandle = self.mock_open()
        self.assertTrue(fhandle.write.called)
        args = fhandle.write.call_args[0]
        self.assertEqual(len(args), 1)
        file_content = args[0].strip()
        pattern = r"SECRET_KEY = '[0-9a-f-]{36}'"
        self.assertIsNotNone(re.match(pattern, file_content))
