import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))

# Directory to stash log files in
LOG_DIR = os.path.join(ROOT, 'log')

# Directory to stash pid files in
RUN_DIR = os.path.join(ROOT, 'run')

# Web Service
WEB_HOST = 'localhost'
WEB_PORT = 8900
