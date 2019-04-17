from django.conf.urls import include, url

from localshop.accounts import views

app_name = "accounts"
urlpatterns = [
    url('^profile/$', views.ProfileView.as_view(), name='profile'),
    url('^access-keys/$', views.AccessKeyListView.as_view(), name='access_key_list'),
    url('^access-keys/new$', views.AccessKeyCreateView.as_view(), name='access_key_create'),
    url('^access-keys/(?P<pk>\d+)/', include([
        url('^secret$', views.AccessKeySecretView.as_view(), name='access_key_secret'),
        url('^edit$', views.AccessKeyUpdateView.as_view(), name='access_key_edit'),
        url('^delete$', views.AccessKeyDeleteView.as_view(), name='access_key_delete'),
    ])),

    url('^teams/$', views.TeamListView.as_view(), name='team_list'),
    url('^teams/create$', views.TeamCreateView.as_view(), name='team_create'),
    url('^teams/(?P<pk>\d+)/', include([
        url('^$', views.TeamDetailView.as_view(), name='team_detail'),
        url('^edit$', views.TeamUpdateView.as_view(), name='team_edit'),
        url('^delete$', views.TeamDeleteView.as_view(), name='team_delete'),
        url('^member-add$', views.TeamMemberAddView.as_view(), name='team_member_add'),
        url('^member-remove$', views.TeamMemberRemoveView.as_view(), name='team_member_remove'),
    ]))
]
