from django.conf.urls import url

from localshop.apps.permissions import views


urlpatterns = [
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

    url('^teams/$', views.TeamListView.as_view(), name='team_list'),
    url('^teams/create$', views.TeamCreateView.as_view(), name='team_create'),
    url('^teams/(?P<pk>\d+)/$', views.TeamDetailView.as_view(), name='team_detail'),
    url('^teams/(?P<pk>\d+)/edit$', views.TeamUpdateView.as_view(), name='team_edit'),
    url('^teams/(?P<pk>\d+)/delete$', views.TeamDeleteView.as_view(), name='team_delete'),
]
