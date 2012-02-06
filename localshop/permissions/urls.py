from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from localshop.permissions import views


urlpatterns = patterns('',
    url(r'^login/$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),

    url('^users$', views.UserListView.as_view(), name='user_index'),

    url(r'^users/(?P<pk>\d+)$',
        views.UserDetailView.as_view(),
        name='user_show'),

    url(r'^users/create$',
        views.UserCreateView.as_view(),
        name='user_create'),

    url(r'^users/(?P<pk>\d+)/edit$',
        views.UserUpdateView.as_view(), name='user_edit'),

    url(r'^cidr/$', views.CidrListView.as_view(), name='cidr_index'),

    url(r'^cidr/create$', views.CidrCreateView.as_view(), name='cidr_create'),
    url(r'^cidr/(?P<pk>\d+)/edit', views.CidrUpdateView.as_view(),
        name='cidr_edit'),
    url(r'^cidr/(?P<pk>\d+)/delete', views.CidrDeleteView.as_view(),
        name='cidr_delete'),
)
