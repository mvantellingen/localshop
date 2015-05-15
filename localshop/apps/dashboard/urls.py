from django.conf.urls import url

from localshop.apps.dashboard import views


urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),

    url('^repositories/$', views.RepositoryListView.as_view(), name='repository_list'),
    url('^repositories/create$', views.RepositoryCreateView.as_view(), name='repository_create'),
    url('^repositories/(?P<slug>[^/]+)/$', views.RepositoryDetailView.as_view(), name='repository_detail'),
    url('^repositories/(?P<slug>[^/]+)/edit$', views.RepositoryUpdateView.as_view(), name='repository_edit'),
    url('^repositories/(?P<slug>[^/]+)/delete$', views.RepositoryDeleteView.as_view(), name='repository_delete'),



    url('^repositories/(?P<repo>[^/]+)/packages/(?P<name>[-\._\w]+)/$',
        views.PackageDetail.as_view(), name='package_detail'),

]
