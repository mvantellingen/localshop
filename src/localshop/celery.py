import celery  # noqa isort:skip
from django.conf import settings  # noqa isort:skip


app = celery.Celery('localshop')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
