"""Runs migrate, creates an admin user and a global CIDR permission.

This command is called by the app.json file as a post installitation script
after the app is deployed to Heroku. You should not need to call this directly."""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import IntegrityError

from localshop.apps.permissions.models import CIDR


class Command(BaseCommand):
    help = __doc__

    def handle(self, *args, **options):

        self.stdout.write('Running migrate')
        call_command('migrate', interactive=False, no_color=True)

        self.stdout.write('Creating localshop admin user.')
        try:
            User.objects.create_superuser('localshop', 'localshop@localshop.com', 'localshop')
        except IntegrityError:
            self.stdout.write('Admin already created.')

        self.stdout.write('Creating 0.0.0.0/0 CIDR permissions.')
        CIDR.objects.get_or_create(cidr='0.0.0.0/0', defaults={'require_credentials': False})
