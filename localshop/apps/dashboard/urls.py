from django.conf.urls import include, url

from localshop.apps.dashboard import views


urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),

    url('^repositories/create$', views.RepositoryCreateView.as_view(), name='repository_create'),
    url('^repositories/(?P<slug>[^/]+)/$', views.RepositoryDetailView.as_view(), name='repository_detail'),
    url('^repositories/(?P<slug>[^/]+)/edit$', views.RepositoryUpdateView.as_view(), name='repository_edit'),
    url('^repositories/(?P<slug>[^/]+)/delete$', views.RepositoryDeleteView.as_view(), name='repository_delete'),
    url('^repositories/(?P<repo>[^/]+)/packages/(?P<name>[-\._\w]+)/$',
        views.PackageDetail.as_view(), name='package_detail'),

    url('^repositories/(?P<repo>[^/]+)/package-add/$',
        views.PackageAddView.as_view(), name='package_add'),

    url(r'^repositories/(?P<repo>[^/]+)/settings/',
        include([
            url(r'^cidr/$', views.CidrListView.as_view(), name='cidr_index'),
            url(r'^cidr/create$', views.CidrCreateView.as_view(), name='cidr_create'),
            url(r'^cidr/(?P<pk>\d+)/edit', views.CidrUpdateView.as_view(), name='cidr_edit'),
            url(r'^cidr/(?P<pk>\d+)/delete', views.CidrDeleteView.as_view(), name='cidr_delete'),

            url(r'^credentials/$', views.CredentialListView.as_view(),
                name='credential_index'),
            url(r'^credentials/create$', views.CredentialCreateView.as_view(),
                name='credential_create'),
            url(r'^credentials/(?P<access_key>[a-f0-9]+)/secret', views.CredentialSecretKeyView.as_view(),
                name='credential_secret'),
            url(r'^credentials/(?P<access_key>[a-f0-9]+)/edit', views.CredentialUpdateView.as_view(),
                name='credential_edit'),
            url(r'^credentials/(?P<access_key>[a-f0-9]+)/delete', views.CredentialDeleteView.as_view(),
                name='credential_delete'),

            url(r'^teams/$', views.TeamAccessView.as_view(), name='team_access'),

        ], namespace='repo_settings')),

]
