import re
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from localshop.apps.packages.xmlrpc import handle_request

admin.autodiscover()

static_prefix = re.escape(settings.STATIC_URL.lstrip('/'))


urlpatterns = patterns('',
    url(r'^$', 'localshop.views.index', name='index'),

    # Default path for xmlrpc calls
    url(r'^RPC2$', handle_request),

    url(r'^packages/',
        include('localshop.apps.packages.urls', namespace='packages')),

    url(r'^simple/', include('localshop.apps.packages.urls_simple',
        namespace='packages-simple')),

    # We add a separate route for simple without the trailing slash so that
    # POST requests to /simple/ and /simple both work
    url(r'^simple$', 'localshop.apps.packages.views.simple_index'),

    url(r'^permissions/',
        include('localshop.apps.permissions.urls', namespace='permissions')),

    url(r'^accounts/signup/', RedirectView.as_view(url="/")),

    url(r'^accounts/', include('userena.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^%s(?P<path>.*)$' % static_prefix,
        'django.contrib.staticfiles.views.serve', {'insecure': True}),
)
