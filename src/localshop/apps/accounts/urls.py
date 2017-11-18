from django.conf.urls import url

from localshop.apps.accounts import views

urlpatterns = [
    url('^profile/$', views.ProfileView.as_view(), name='profile'),
    url('^access-keys/$', views.AccessKeyListView.as_view(), name='access_key_list'),
    url('^access-keys/new$', views.AccessKeyCreateView.as_view(), name='access_key_create'),
    url('^access-keys/(?P<pk>\d+)/secret$', views.AccessKeySecretView.as_view(), name='access_key_secret'),
    url('^access-keys/(?P<pk>\d+)/edit$', views.AccessKeyUpdateView.as_view(), name='access_key_edit'),
    url('^access-keys/(?P<pk>\d+)/delete$', views.AccessKeyDeleteView.as_view(), name='access_key_delete'),

    url('^teams/$', views.TeamListView.as_view(), name='team_list'),
    url('^teams/create$', views.TeamCreateView.as_view(), name='team_create'),
    url('^teams/(?P<pk>\d+)/$', views.TeamDetailView.as_view(), name='team_detail'),
    url('^teams/(?P<pk>\d+)/edit$', views.TeamUpdateView.as_view(), name='team_edit'),
    url('^teams/(?P<pk>\d+)/delete$', views.TeamDeleteView.as_view(), name='team_delete'),
    url('^teams/(?P<pk>\d+)/member-add$', views.TeamMemberAddView.as_view(), name='team_member_add'),
    url('^teams/(?P<pk>\d+)/member-remove$', views.TeamMemberRemoveView.as_view(), name='team_member_remove'),
]
