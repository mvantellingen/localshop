from logan.runner import run_app
import os


def generate_settings(root):
    def _generate_settings():
        """
        This command is run when ``default_path`` doesn't exist, or ``init`` is
        run and returns a string representing the default data to put into their
        settings file.
        """

        if root:
            config = {
                'root_dir': "'/var/localshop'",
                'web_port': 80,
                'log_dir': "'/var/log/localshop'",
                'run_dir': "'/var/run/localshop'",
            }
        else:
           config = {
                'root_dir': "os.path.dirname(__file__)",
                'web_port': 8900,
                'log_dir': "os.path.join(ROOT, 'log')",
                'run_dir': "os.path.join(ROOT, 'run')",
            }

        CONFIG_TEMPLATE = """
import os.path

from localshop.conf.server import *

ROOT = {root_dir}

DATABASES = {{
    'default': {{
        # You can swap out the engine for MySQL easily by changing this value
        # to ``django.db.backends.mysql`` or to PostgreSQL with
        # ``django.db.backends.postgresql_psycopg2``
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT, 'localshop.db'),
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }}
}}

# Where the packages are stored
MEDIA_ROOT = os.path.join(ROOT, 'files')

LOCALSHOP_WEB_HOST = '0.0.0.0'
LOCALSHOP_WEB_PORT = {web_port:d}

LOG_DIR = {log_dir}
RUN_DIR = {run_dir}

# If the root directory doesn't exist (i.e. we're running as root), create it
if not os.path.exists(ROOT):
    os.makedirs(ROOT)

# If the log or run directories don't exist, create them since supervisord won't
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
if not os.path.exists(RUN_DIR):
    os.makedirs(RUN_DIR)
        """.format(**config)

        return CONFIG_TEMPLATE

    return _generate_settings


def main():
    if hasattr(os, 'getuid') and os.getuid() == 0:
        default_config_path = '/etc/localshop/localshop.conf.py'
        root = True
    else:
        default_config_path = '~/.localshop/localshop.conf.py'
        root = False

    run_app(
        project='localshop',
        default_config_path=default_config_path,
        default_settings='localshop.conf.defaults',
        settings_initializer=generate_settings(root=root),
        settings_envvar='LOCALSHOP_CONF',
    )

if __name__ == '__main__':
    main()
