from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordChangeDoneView, \
    PasswordChangeView, PasswordResetConfirmView, PasswordResetCompleteView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from localshop.apps.accounts.views import login as login_view

urlpatterns = [
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^password_change/$', PasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change/done/$', PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^password_reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
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
