import os
import re

import mock

from django.test import TestCase

from . import CommonCommandsTestMixin, call_command_real as call_command

TEST_HOME = os.path.join(os.path.dirname(__file__), 'home')
MOCK_ENV = {'LOCALSHOP_HOME': TEST_HOME}
DEFAULT_PATH = os.path.expanduser('~/.localshop')


class TestInitCommand(CommonCommandsTestMixin, TestCase):
    def setUp(self):
        super(TestInitCommand, self).setUp()

        patch_environ = mock.patch.dict('os.environ', MOCK_ENV)
        patch_mkdir = mock.patch('os.mkdir')
        patch_open = mock.patch('localshop.management.commands.init.open',
                                mock.mock_open(), create=True)

        self.mock_environ = patch_environ.start()
        self.mock_mkdir = patch_mkdir.start()
        self.mock_open = patch_open.start()

        self.addCleanup(patch_environ.stop)
        self.addCleanup(patch_mkdir.stop)
        self.addCleanup(patch_open.stop)

    def test_default_commands_called(self):
        call_command('init')
        self.assertEqual(self.mock_call.call_count, 3)
        self.mock_call.assert_any_call(
            'syncdb', database='default',
            interactive=False)
        self.mock_call.assert_any_call(
            'migrate', database='default',
            interactive=False)
        self.mock_call.assert_any_call(
            'createsuperuser', database='default',
            interactive=True)

    def test_nosuperuser_commands_called(self):
        call_command('init', nosuperuser=True)
        self.assertEqual(self.mock_call.call_count, 2)
        self.mock_call.assert_any_call(
            'syncdb', database='default',
            interactive=False)
        self.mock_call.assert_any_call(
            'migrate', database='default',
            interactive=False)

    def test_make_dir(self):
        call_command('init')
        self.mock_mkdir.assert_called_once_with(TEST_HOME)

    def test_config_file_contents(self):
        call_command('init')
        test_file = os.path.join(TEST_HOME, 'localshop.conf.py')
        self.mock_open.assert_called_once_with(test_file, 'w')
        fhandle = self.mock_open()
        self.assertTrue(fhandle.write.called)
        args = fhandle.write.call_args[0]
        self.assertEqual(len(args), 1)
        file_content = args[0].strip()
        pattern = r"SECRET_KEY = '[0-9a-f-]{36}'"
        self.assertIsNotNone(re.match(pattern, file_content))

    @mock.patch('os.path.exists')
    def test_default_path(self, mock_path_exists):
        mock_path_exists.return_value = False
        del os.environ['LOCALSHOP_HOME']
        call_command('init')
        self.assertEqual(mock_path_exists.call_count, 2)
        mock_path_exists.assert_any_call(DEFAULT_PATH)
        self.mock_mkdir.assert_called_once_with(DEFAULT_PATH)
        test_file = os.path.join(DEFAULT_PATH, 'localshop.conf.py')
        mock_path_exists.assert_any_call(test_file)
        self.mock_open.assert_called_once_with(test_file, 'w')
