from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        call_command('syncdb', database='default', interactive=False)

        if 'south' in settings.INSTALLED_APPS:
            call_command('migrate', database='default', interactive=False,
                delete_ghosts=True)
