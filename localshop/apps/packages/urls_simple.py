from django.conf.urls import patterns, url

urlpatterns = patterns('localshop.apps.packages.views',
    url(r'^$', 'simple_index', name='simple_index'),
    url(r'^(?P<slug>[-\._\w]+)/?(?P<version>.*?)/?$', 'simple_detail',
        name='simple_detail')
)
