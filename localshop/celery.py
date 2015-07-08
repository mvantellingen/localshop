from __future__ import absolute_import
import os

import celery
from configurations.importer import install as configurations_install


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'localshop.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Localshop')

configurations_install(check_options=True)

from django.conf import settings  # NOQA


app = celery.Celery('localshop')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
