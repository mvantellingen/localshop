from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^packages/',
        include('localshop.packages.urls', namespace='packages')),

    url(r'^simple/', include('localshop.packages.urls_simple',
        namespace='packages-simple')),


    url(r'^admin/', include(admin.site.urls)),
)
