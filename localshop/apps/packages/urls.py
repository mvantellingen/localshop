from django.conf.urls import url
from django.views.decorators.cache import cache_page

from localshop.apps.packages import views


urlpatterns = [
    url(r'^(?P<repo>[-\._\w]+)/?$', views.SimpleIndex.as_view(),
        name='simple_index'),

    url(r'^(?P<repo>[-\._\w\s]+)/(?P<slug>[-\._\w]+)/$',
        cache_page(60)(views.SimpleDetail.as_view()),
        name='simple_detail'),

    url(r'^(?P<repo>[-\._\w\s]+)/download/(?P<name>[-\._\w]+)/(?P<pk>\d+)/(?P<filename>.*)$',
        views.DownloadReleaseFile.as_view(), name='download'),

    url(r'^(?P<repo>[-\._\w\s]+)/refresh/(?P<name>[-\._\w]+)',
        views.PackageRefreshView.as_view(), name='refresh'),
]
