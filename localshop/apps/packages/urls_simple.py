from django.conf.urls import url
from django.views.decorators.cache import cache_page

from localshop.apps.packages import views


urlpatterns = [
    url(r'^(?P<repo>[-\._\w]+)/?$', views.SimpleIndex.as_view(),
        name='simple_index'),

    url(r'^(?P<repo>[-\._\w]+)/(?P<slug>[-\._\w]+)/$',
        cache_page(60)(views.SimpleDetail.as_view()),
        name='simple_detail')
]
