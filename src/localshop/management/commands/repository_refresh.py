from django.core.management.base import BaseCommand

from localshop.packages import tasks


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        tasks.refresh_repository_mirrors()
