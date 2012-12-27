from django.conf.urls.defaults import patterns, url

from localshop.apps.packages import views


urlpatterns = patterns('',
    url(r'^$', views.SimpleIndex.as_view(), name='simple_index'),
    url(r'^(?P<slug>[^/]+)/(?P<version>.*?)$', views.SimpleDetail.as_view(),
        name='simple_detail')
)
