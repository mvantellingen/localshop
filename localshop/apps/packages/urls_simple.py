from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from localshop.apps.packages import views


urlpatterns = [
    url(r'^$', views.SimpleIndex.as_view(), name='simple_index'),
    url(r'^(?P<slug>[-\._\w]+)/$', cache_page(60)(views.SimpleDetail.as_view()),
        name='simple_detail')
]
