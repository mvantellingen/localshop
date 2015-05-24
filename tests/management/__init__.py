from copy import deepcopy
import os

import mock

from django.core import management

TEST_HOME = os.path.join(os.path.dirname(__file__), 'home')
MOCK_ENV = {'LOCALSHOP_HOME': TEST_HOME}
call_command_real = deepcopy(management.call_command)
const_mock = mock.MagicMock()


class CommonCommandsTestMixin(object):

    def setUp(self):
        super(CommonCommandsTestMixin, self).setUp()

        patch_call_command = mock.patch('django.core.management.call_command',
                                        const_mock)

        self.mock_call = patch_call_command.start()

        self.addCleanup(patch_call_command.stop)
        self.addCleanup(self.mock_call.reset_mock)

        self.assertNotEqual(self.mock_call, call_command_real)
