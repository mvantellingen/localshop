import urlparse
from django.utils.crypto import get_random_string

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now


def clean_redirect_url(request, url, default='/'):
    """ Use default setting if redirect_to is empty else do a
    security check -- don't allow redirection to a different
    host.

    """
    netloc = urlparse.urlparse(url)[1]
    if not url or (netloc and netloc != request.get_host()):
        url = default
    return url


def generate_settings():
    """
    This command is run when ``default_path`` doesn't exist, or ``init`` is
    run and returns a string representing the default data to put into their
    settings file.
    """
    CONFIG_TEMPLATE = """
import os.path

ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
        # You can swap out the engine for MySQL easily by changing this value
        # to ``django.db.backends.mysql`` or to PostgreSQL with
        # ``django.db.backends.postgresql_psycopg2``
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT, 'localshop.db'),
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Where the packages are stored
MEDIA_ROOT = os.path.join(ROOT, 'files')
# *DON'T set MEDIA_URL since we don't want to serve those files directly
# but only through a view to reduce the chance of a security breach

STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(ROOT, 'assets')

# Comment out the following lines to enable the optional credential system
# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     'localshop.apps.permissions.backend.CredentialBackend',
# ]

SECRET_KEY = '%(secret_key)s'

    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    values = {'secret_key': get_random_string(50, chars)}
    return CONFIG_TEMPLATE % values
