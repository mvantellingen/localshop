from django.conf.urls.defaults import patterns, include, url

from localshop.packages import views


urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^(?P<name>[^/]+)/$', views.Detail.as_view(), name='detail'),

    url(r'^(?P<name>[^/]+)/refresh',
        views.refresh, name='refresh'),
    url(r'^(?P<name>[^/]+)/download/(?P<pk>\d+)/(?P<filename>.*)$',
        views.download_file, name='download'),
)
