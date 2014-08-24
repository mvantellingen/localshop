import os
import imp
from celery.schedules import crontab

import djcelery
djcelery.setup_loader()

from configurations import Settings
from configurations.utils import uppercase_attributes

try:
    DEFAULT_PATH = os.environ['LOCALSHOP_HOME']
except KeyError:
    DEFAULT_PATH = os.path.expanduser('~/.localshop')


def FileSettings(path):
    path = os.path.expanduser(path)
    mod = imp.new_module('localshop.local')
    mod.__file__ = path

    class Holder(object):
        pass

    try:
        with open(path, 'r') as fh:
            exec(fh.read(), mod.__dict__)
    except IOError as e:
        print("Notice: Unable to load configuration file %s (%s), "
              "using default settings\n\n" % (path, e.strerror))
        return Holder

    for name, value in uppercase_attributes(mod).items():
        setattr(Holder, name, value)

    return Holder


class Base(Settings):
    # Django settings for localshop project.
    PROJECT_ROOT = os.path.join(os.path.dirname(__file__), os.pardir)

    DEBUG = False
    TEMPLATE_DEBUG = DEBUG

    ADMINS = (
        # ('Your Name', 'your_email@example.com'),
    )

    MANAGERS = ADMINS

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(DEFAULT_PATH, 'localshop.db'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

    # Local time zone for this installation. Choices can be found here:
    # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
    # although not all choices may be available on all operating systems.
    # On Unix systems, a value of None will cause Django to use the same
    # timezone as the operating system.
    # If running in a Windows environment this must be set to the same as your
    # system time zone.
    TIME_ZONE = 'Europe/Amsterdam'

    # Language code for this installation. All choices can be found here:
    # http://www.i18nguy.com/unicode/language-identifiers.html
    LANGUAGE_CODE = 'en-us'

    SITE_ID = 1

    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = True

    # If you set this to False, Django will not format dates, numbers and
    # calendars according to the current locale.
    USE_L10N = True

    # If you set this to False, Django will not use timezone-aware datetimes.
    USE_TZ = True

    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Example: "/home/media/media.lawrence.com/media/"
    # MEDIA_ROOT = 'files'

    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/home/media/media.lawrence.com/static/"
    # STATIC_ROOT = 'assets'

    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"
    STATIC_URL = '/assets/'

    # Additional locations of static files
    STATICFILES_DIRS = [
        os.path.join(PROJECT_ROOT, 'static')
    ]

    # List of finder classes that know how to find static files in
    # various locations.
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'CHANGE-ME'

    # List of callables that know how to import templates from various sources.
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        #'django.template.loaders.eggs.Loader',
    )

    TEMPLATE_CONTEXT_PROCESSORS = [
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.contrib.messages.context_processors.messages',

        'localshop.apps.packages.context_processors.sidebar',
    ]

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

    ROOT_URLCONF = 'localshop.urls'

    # Python dotted path to the WSGI application used by Django's runserver.
    WSGI_APPLICATION = 'localshop.wsgi.application'

    TEMPLATE_DIRS = (
        os.path.join(PROJECT_ROOT, 'localshop', 'templates'),
    )

    BROKER_URL = "django://"

    CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
    CELERYD_FORCE_EXECV = False
    CELERYBEAT_SCHEDULE = {
        # Executes every day at 1:00 AM
        'every-day-1am': {
            'task': 'localshop.apps.packages.tasks.update_packages',
            'schedule': crontab(hour=1, minute=0),
        },
    }

    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',

        'kombu.transport.django',
        'djcelery',
        'south',
        'gunicorn',
        'userena',
        'guardian',

        'localshop',
        'localshop.apps.packages',
        'localshop.apps.permissions',
    ]

    # Auth settings
    AUTHENTICATION_BACKENDS = (
        'userena.backends.UserenaAuthenticationBackend',
        'guardian.backends.ObjectPermissionBackend',
        'localshop.apps.permissions.backend.CredentialBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    AUTH_PROFILE_MODULE = 'permissions.AuthProfile'
    LOGIN_URL = '/accounts/signin/'
    LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
    LOGOUT_URL = '/accounts/signout'
    USERENA_MUGSHOT_GRAVATAR = True
    USERENA_MUGSHOT_SIZE = 20
    ANONYMOUS_USER_ID = -1

    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler'
            },
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
    }

    ALLOWED_HOSTS = ['*']

    LOCALSHOP_DELETE_FILES = False

    LOCALSHOP_DISTRIBUTION_STORAGE = 'storages.backends.overwrite.OverwriteStorage'

    LOCALSHOP_PYPI_URL = 'https://pypi.python.org/pypi'

    LOCALSHOP_HTTP_PROXY = None

    LOCALSHOP_ISOLATED = False


class TestConfig(Base):
    SECRET_KEY = "TEST-KEY"


class Localshop(FileSettings(os.path.join(DEFAULT_PATH, 'localshop.conf.py')), Base):
    pass
