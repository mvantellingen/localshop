from django.conf.urls.defaults import patterns, include, url

from localshop.packages import views


urlpatterns = patterns('',

    url(r'^download/(?P<pk>\d+)/(?P<filename>.*)$',
        views.download_file, name='download')
)
