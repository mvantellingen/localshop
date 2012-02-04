from django.conf.urls.defaults import patterns, include, url

from localshop.packages import views


urlpatterns = patterns('',
    url('^$', views.SimpleIndex.as_view(), name='simple_index'),
    url('^(?P<slug>[^/]+)/$', views.SimpleDetail.as_view(),
        name='simple_detail')
)

