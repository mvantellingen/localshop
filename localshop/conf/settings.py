from localshop.conf.defaults import *

from django.conf import settings


for k in dir(settings):
    if k.startswith('LOCALSHOP_'):
        locals()[k.split('LOCALSHOP_', 1)[1]] = getattr(settings, k)
