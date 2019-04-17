from django.conf.urls import url
from django.views.decorators.cache import cache_page

from localshop.packages import views

app_name = "packages"
urlpatterns = [
    url(r'^(?P<repo>[-\._\w]+)/?$', views.SimpleIndex.as_view(),
        name='simple_index'),

    url(r'^(?P<repo>[-\._\w]+)/(?P<slug>[-\._\w]+)/$',
        cache_page(60)(views.SimpleDetail.as_view()),
        name='simple_detail'),

    url(r'^(?P<repo>[-\._\w]+)/download/(?P<name>[-\._\w]+)/(?P<pk>\d+)/(?P<filename>.*)$',
        views.DownloadReleaseFile.as_view(), name='download'),
]
