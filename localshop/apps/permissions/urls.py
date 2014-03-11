from django.conf.urls import patterns, url

from localshop.apps.permissions import views


urlpatterns = patterns('',
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
    url(r'^credentials/(?P<access_key>[a-f0-9]+)/edit', views.CredentialUpdateView.as_view(),
        name='credential_edit'),
    url(r'^credentials/(?P<access_key>[a-f0-9]+)/delete', views.CredentialDeleteView.as_view(),
        name='credential_delete'),
)
