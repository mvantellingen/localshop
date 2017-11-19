import os

import mock
from django.test import TestCase

from . import call_command_real as call_command
from . import CommonCommandsTestMixin

DEFAULT_PATH = os.path.expanduser('~/.localshop')


class TestInitCommand(CommonCommandsTestMixin, TestCase):
    def setUp(self):
        super(TestInitCommand, self).setUp()

        patch_mkdir = mock.patch('os.mkdir')
        patch_open = mock.patch('localshop.management.commands.init.open',
                                mock.mock_open(), create=True)

        self.mock_mkdir = patch_mkdir.start()
        self.mock_open = patch_open.start()

        self.addCleanup(patch_mkdir.stop)
        self.addCleanup(patch_open.stop)

    def test_default_commands_called(self):
        call_command('init')
        self.assertEqual(self.mock_call.call_count, 2)
        self.mock_call.assert_any_call(
            'migrate', database='default', interactive=False)
