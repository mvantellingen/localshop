from django.core.management import call_command
from django.conf import settings

from localshop.commands.utils import options, opt


@options(
    opt('--interactive', default=False, action='store_true'),
    opt('--delete-ghost-migrations', default=True, dest='delete_ghosts'),
)
def upgrade(interactive=True, delete_ghosts=True):
    call_command('syncdb', database='default', interactive=interactive)

    if 'south' in settings.INSTALLED_APPS:
        call_command('migrate', database='default', interactive=interactive,
            delete_ghosts=delete_ghosts)
