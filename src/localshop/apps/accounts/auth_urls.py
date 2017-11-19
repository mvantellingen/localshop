from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from localshop.apps.accounts.views import login as login_view

urlpatterns = [
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
]

if settings.OAUTH2_PROVIDER:
    urlpatterns.append(
        url(r'^login/$', RedirectView.as_view(
            url=reverse_lazy('social:begin', kwargs={
                'backend': settings.OAUTH2_PROVIDER
            }),
        ), name='login')
    )
else:
    urlpatterns.append(url(r'^login/$', login_view, name='login'))
