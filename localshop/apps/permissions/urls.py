from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from localshop.apps.permissions import views


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

    url(r'^credentials/$', views.CredentialListView.as_view(),
        name='credential_index'),
    url(r'^credentials/create$', views.create_credential,
        name='credential_create'),
    url(r'^credentials/(?P<access_key>[a-f0-9]+)/activate', views.activate_credential,
        name='credential_activate'),
    url(r'^credentials/(?P<access_key>[a-f0-9]+)/deactivate', views.deactivate_credential,
        name='credential_deactivate'),
    url(r'^credentials/(?P<access_key>[a-f0-9]+)/secret', views.secret_key,
        name='credential_secret'),
    url(r'^credentials/(?P<access_key>[a-f0-9]+)/delete', views.CredentialDeleteView.as_view(),
        name='credential_delete'),
)
