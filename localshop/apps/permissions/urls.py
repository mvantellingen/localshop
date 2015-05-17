from django.conf.urls import url

from localshop.apps.permissions import views


urlpatterns = [

    url('^teams/$', views.TeamListView.as_view(), name='team_list'),
    url('^teams/create$', views.TeamCreateView.as_view(), name='team_create'),
    url('^teams/(?P<pk>\d+)/$', views.TeamDetailView.as_view(), name='team_detail'),
    url('^teams/(?P<pk>\d+)/edit$', views.TeamUpdateView.as_view(), name='team_edit'),
    url('^teams/(?P<pk>\d+)/delete$', views.TeamDeleteView.as_view(), name='team_delete'),
    url('^teams/(?P<pk>\d+)/member-add$', views.TeamMemberAddView.as_view(), name='team_member_add'),
    url('^teams/(?P<pk>\d+)/member-remove$', views.TeamMemberRemoveView.as_view(), name='team_member_remove'),
]
