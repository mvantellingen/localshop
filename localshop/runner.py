from logan.runner import run_app


def generate_settings():
    """
    This command is run when ``default_path`` doesn't exist, or ``init`` is
    run and returns a string representing the default data to put into their
    settings file.
    """
    CONFIG_TEMPLATE = """
import os.path

from localshop.conf.server import *

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

    """
    return CONFIG_TEMPLATE


def main():
    run_app(
        project='localshop',
        default_config_path='~/.localshop/localshop.conf.py',
        default_settings='localshop.conf.defaults',
        settings_initializer=generate_settings,
        settings_envvar='LOCALSHOP_CONF',
    )

if __name__ == '__main__':
    main()
