from django.conf.urls import include, url

from localshop.dashboard import views

app_name = "dashboard"
repository_urls = [
    # Package urls
    url('^packages/add/$',
        views.PackageAddView.as_view(),
        name='package_add'),
    url('^packages/(?P<name>[-\._\w]+)/', include([
        url('^$',
            views.PackageDetailView.as_view(),
            name='package_detail'),
        url('^refresh-from-upstream/$',
            views.PackageRefreshView.as_view(),
            name='package_refresh'),
        url('^release-mirror-file/$',
            views.PackageMirrorFileView.as_view(),
            name='package_mirror_file'),
    ])),

    # Settings
    url(r'^settings/', include(([

        # CIDR
        url(r'^cidr/$',
            views.CidrListView.as_view(), name='cidr_index'),
        url(r'^cidr/create$',
            views.CidrCreateView.as_view(), name='cidr_create'),
        url(r'^cidr/(?P<pk>\d+)/edit',
            views.CidrUpdateView.as_view(), name='cidr_edit'),
        url(r'^cidr/(?P<pk>\d+)/delete',
            views.CidrDeleteView.as_view(), name='cidr_delete'),

        # Credentials
        url(r'^credentials/$',
            views.CredentialListView.as_view(),
            name='credential_index'),
        url(r'^credentials/create$',
            views.CredentialCreateView.as_view(),
            name='credential_create'),
        url(r'^credentials/(?P<access_key>[-a-f0-9]+)/secret',
            views.CredentialSecretKeyView.as_view(),
            name='credential_secret'),
        url(r'^credentials/(?P<access_key>[-a-f0-9]+)/edit',
            views.CredentialUpdateView.as_view(),
            name='credential_edit'),
        url(r'^credentials/(?P<access_key>[-a-f0-9]+)/delete',
            views.CredentialDeleteView.as_view(),
            name='credential_delete'),

        url(r'^teams/$', views.TeamAccessView.as_view(), name='team_access'),

    ], "dashboard"), namespace='repo_settings')),
]

urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
    url('^repositories/create$', views.RepositoryCreateView.as_view(), name='repository_create'),

    url('^repositories/(?P<slug>[^/]+)/', include([
        url('^$', views.RepositoryDetailView.as_view(), name='repository_detail'),
        url('^edit$', views.RepositoryUpdateView.as_view(), name='repository_edit'),
        url('^delete$', views.RepositoryDeleteView.as_view(), name='repository_delete'),
        url('^refresh$', views.RepositoryRefreshView.as_view(), name='repository_refresh'),
    ])),

    url('^repositories/(?P<repo>[^/]+)/', include(repository_urls))

]
