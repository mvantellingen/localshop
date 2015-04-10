import os
import shutil
import tempfile
import logging
from functools import wraps

from django.conf import settings
from django.test.utils import override_settings
from django.core.cache import cache


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


def generate_key(function, *args, **kwargs):
    args_string = ','.join([str(arg) for arg in args] +
                           ['{}={}'.format(k, v) for k, v in kwargs.items()])
    return '{}({})'.format(function.__name__, args_string)


def enqueue(function, *args, **kwargs):
    key = generate_key(function, *args, **kwargs)
    logging.info('key %s', key)

    if cache.get(key):
        logging.info('Dropping task %s', key)
        return

    cache.set(key, 'lock')
    function.delay(*args, **kwargs)


def no_duplicates(function, *args, **kwargs):
    """
    Makes sure that no duplicated tasks are enqueued.
    """
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        key = generate_key(function, *args, **kwargs)
        try:
            function(self, *args, **kwargs)
        finally:
            logging.info('Removing key %s', key)
            cache.delete(key)

    return wrapper
