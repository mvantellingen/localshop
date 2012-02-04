from localshop.commands.utils import consume_args


@consume_args
def manage(args):
    from django.core.management import ManagementUtility
    utility = ManagementUtility(args)
    utility.execute()


def update_migrations():
    """
    Creates schemamigrations for localshop.
    """
    from django.core.management import ManagementUtility
    args = 'manage.py schemamigration localshop --auto'.split(' ')
    utility = ManagementUtility(args)
    utility.execute()
