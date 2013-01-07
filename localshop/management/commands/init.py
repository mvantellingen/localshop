import os.path
import uuid

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        default_path = os.path.expanduser('~/.localshop')

        if not os.path.exists(default_path):
            os.mkdir(default_path)

        config_path = os.path.join(default_path, 'localshop.conf.py')
        if not os.path.exists(config_path):
            default_params = {
                'SECRET_KEY': uuid.uuid4()
            }

            with open(config_path, 'w') as fh:
                fh.write("""
SECRET_KEY = '%(SECRET_KEY)s'

                """ % default_params)

        call_command('syncdb', database='default', interactive=False)
        call_command('migrate', database='default', interactive=False)
        call_command('createsuperuser', database='default', interactive=True)
