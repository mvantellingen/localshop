from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from localshop.accounts import views


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
)
