import os
import shutil
import tempfile

from django.conf import settings
from django.test.utils import override_settings

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now


class TemporaryMediaRootMixin(object):

    def setUp(self):
        super(TemporaryMediaRootMixin, self).setUp()

        # Create path to temp dir and recreate it
        temp_media_root = os.path.join(
            tempfile.gettempdir(), 'project-testrun')
        if os.path.exists(temp_media_root):
            shutil.rmtree(temp_media_root)
        os.mkdir(temp_media_root)

        self.override = override_settings(
            MEDIA_ROOT=temp_media_root,
        )
        self.override.enable()

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)
        self.override.disable()

        super(TemporaryMediaRootMixin, self).tearDown()
