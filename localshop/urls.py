import re
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

static_prefix = re.escape(settings.STATIC_URL.lstrip('/'))


urlpatterns = patterns('',
    url(r'^$', 'localshop.views.index', name='index'),

    url(r'^packages',
        include('localshop.apps.packages.urls', namespace='packages')),

    url(r'^simple/', include('localshop.apps.packages.urls_simple',
        namespace='packages-simple')),

    url(r'^permissions',
        include('localshop.apps.permissions.urls', namespace='permissions')),

    url(r'^accounts/', include('userena.urls')),

    url(r'^admin', include(admin.site.urls)),

    url(r'^%s(?P<path>.*)$' % static_prefix,
        'django.contrib.staticfiles.views.serve', {'insecure': True}),
)
