from django.conf.urls import url

from localshop.apps.packages import views


urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^(?P<name>[-\._\w]+)/$', views.Detail.as_view(), name='detail'),

    url(r'^(?P<name>[-\._\w]+)/refresh',
        views.refresh, name='refresh'),
    url(r'^(?P<name>[-\._\w]+)/download/(?P<pk>\d+)/(?P<filename>.*)$',
        views.download_file, name='download'),
]
