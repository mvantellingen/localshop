from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'localshop.views.frontpage', name='frontpage'),

    url(r'^packages/',
        include('localshop.packages.urls', namespace='packages')),

    url(r'^simple/', include('localshop.packages.urls_simple',
        namespace='packages-simple')),

    url(r'^accounts/',
        include('localshop.accounts.urls', namespace='accounts')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^_static/(?P<path>.*)$', 'localshop.views.static_media',
        name='static'),
)

urlpatterns += staticfiles_urlpatterns()
