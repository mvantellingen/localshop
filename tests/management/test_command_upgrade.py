import mock
from django.conf import settings
from django.test import TestCase

from . import call_command_real as call_command
from . import CommonCommandsTestMixin

global_mock = mock.MagicMock()


class TestInitCommand(CommonCommandsTestMixin, TestCase):
    def setUp(self):
        super(TestInitCommand, self).setUp()
        patch_settings = mock.patch('django.conf.settings', global_mock)
        self.mock_settings = patch_settings.start()
        self.addCleanup(patch_settings.stop)

    def test_default_commands_called(self):
        call_command('upgrade')
        self.assertEqual(self.mock_call.call_count, 1)
        self.mock_call.assert_any_call(
            'syncdb', database='default',
            interactive=False)

    def test_with_south_commands_called(self):
        self.mock_settings.INSTALLED_APPS = settings.INSTALLED_APPS + ['south']
        call_command('upgrade')
        self.assertEqual(self.mock_call.call_count, 2)
        self.mock_call.assert_any_call(
            'syncdb', database='default',
            interactive=False)
        self.mock_call.assert_any_call(
            'migrate', database='default',
            interactive=False, delete_ghosts=True)
