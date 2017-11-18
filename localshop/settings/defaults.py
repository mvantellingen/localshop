import os
import uuid
import imp
from django.contrib import messages
from celery.schedules import crontab
import environ

env = environ.Env()

# Django settings for localshop project.
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

DEBUG = env.bool('DEBUG', default=False)
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': env.db(default='sqlite:///localshop.db'),
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = env.str('TIME_ZONE', default='UTC')

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

STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
STATIC_URL = '/assets/'

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static')
]
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = env.str('SECRET_KEY', default=uuid.uuid4())

SESSION_COOKIE_AGE = 28 * 24 * 60 * 60  # 4 weeks

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]


ROOT_URLCONF = 'localshop.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'localshop.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

BROKER_URL = "django://"

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
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
    'django.contrib.humanize',

    'gunicorn',
    'django_celery_beat',
    'django_celery_results',
    'widget_tweaks',

    'localshop',
    'localshop.apps.accounts',
    'localshop.apps.dashboard',
    'localshop.apps.packages',
    'localshop.apps.permissions',
]

# Auth settings
AUTHENTICATION_BACKENDS = (
    'localshop.apps.accounts.backend.AccessKeyBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_URL = '/accounts/logout'
AUTH_USER_MODEL = 'accounts.User'

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

EMAIL = env.email_url('EMAIL', 'smtp://localhost:25/')

ALLOWED_HOSTS = ['*']

LOCALSHOP_DELETE_FILES = False

LOCALSHOP_HTTP_PROXY = None

LOCALSHOP_ISOLATED = False

LOCALSHOP_RELEASE_OVERWRITE = True

# Use X-Forwarded-For header as the source for the client's IP.
# Use where you have Nginx/Apache/etc as a reverse proxy infront of Localshop/Gunicorn.
LOCALSHOP_USE_PROXIED_IP = False

LOCALSHOP_VERSIONING_TYPE = None
