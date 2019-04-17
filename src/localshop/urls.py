import re

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

import localshop.dashboard.urls
import localshop.packages.urls
from localshop import views
from localshop.packages.views import SimpleIndex
from localshop.packages.xmlrpc import handle_request

admin.autodiscover()

static_prefix = re.escape(settings.STATIC_URL.lstrip('/'))


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/',
        include(localshop.dashboard.urls, namespace='dashboard')),

    # Default path for xmlrpc calls
    url(r'^RPC2$', handle_request),
    url(r'^pypi$', handle_request),

    url(r'^repo/',
        include(localshop.packages.urls, namespace='packages')),

    # Backwards compatible url (except for POST requests)
    url(r'^simple/?$', SimpleIndex.as_view(), {'repo': 'default'}),
    url(r'^simple/(?P<path>.*)',
        RedirectView.as_view(url='/repo/default/%(path)s')),

    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^accounts/', include('localshop.accounts.auth_urls')),
    url(r'^accounts/', include('localshop.accounts.urls', namespace='accounts')),
    url(r'^admin/', admin.site.urls),
]
