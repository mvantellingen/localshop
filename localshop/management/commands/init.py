import os
import uuid

from optparse import make_option

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            "--no-superuser",
            default=False,
            action="store_true",
            dest="nosuperuser",
            help="Doesn't create a superuser and therefore requires no interaction. Useful for deploying using automated tools. You'll need to provide some initial fixtures to actually get access",
        ),
    )

    def handle(self, *args, **kwargs):

        self.nosuperuser = kwargs.get("nosuperuser")

        try:
            default_path = os.environ['LOCALSHOP_HOME']
        except KeyError:
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
        if not self.nosuperuser:
            call_command('createsuperuser', database='default', interactive=True)
