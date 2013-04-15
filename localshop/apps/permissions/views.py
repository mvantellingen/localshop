from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.views.generic import UpdateView, DeleteView

from localshop.views import LoginRequiredMixin, PermissionRequiredMixin
from localshop.utils import now
from localshop.apps.permissions import models


class CidrListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.CIDR
    object_context_name = 'cidrs'
    permission_required = 'permissions.view_cidr'


class CidrCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.CIDR
    permission_required = 'permissions.add_cidr'

    def get_success_url(self):
        return reverse('permissions:cidr_index')


class CidrUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.CIDR
    permission_required = 'permissions.change_cidr'

    def get_success_url(self):
        return reverse('permissions:cidr_index')


class CidrDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.CIDR
    permission_required = 'permissions.delete_cidr'

    def get_success_url(self):
        return reverse('permissions:cidr_index')


class CredentialListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    object_context_name = 'credentials'
    permission_required = 'permissions.view_credential'

    def get_queryset(self):
        return models.Credential.objects.filter(creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CredentialListView, self).get_context_data(**kwargs)
        context['current_url'] = Site.objects.get_current()
        return context


class CredentialUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    class CredentialModelForm(ModelForm):
        class Meta:
            model = models.Credential
            fields = ('comment',)

    model = models.Credential
    form_class = CredentialModelForm
    slug_field = 'access_key'
    slug_url_kwarg = 'access_key'
    permission_required = 'permissions.change_credential'

    def get_object(self, queryset=None):
        obj = super(CredentialUpdateView, self).get_object(queryset)
        if not obj.creator == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('permissions:credential_index')


class CredentialDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Credential
    slug_field = 'access_key'
    slug_url_kwarg = 'access_key'
    permission_required = 'permissions.delete_credential'

    def get_object(self, queryset=None):
        obj = super(CredentialDeleteView, self).get_object(queryset)
        if not obj.creator == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('permissions:credential_index')


@permission_required('permissions.add_credential')
@login_required
def create_credential(request):
    models.Credential.objects.create(creator=request.user)
    return redirect('permissions:credential_index')


@permission_required('permissions.add_credential')
@login_required
def secret_key(request, access_key):
    if not request.is_ajax():
        raise SuspiciousOperation
    credential = get_object_or_404(models.Credential,
                                   creator=request.user,
                                   access_key=access_key)
    return HttpResponse(credential.secret_key)


@permission_required('permissions.change_credential')
@login_required
def activate_credential(request, access_key):
    credential = get_object_or_404(models.Credential,
                                   creator=request.user,
                                   access_key=access_key)
    credential.deactivated = None
    credential.save()
    return redirect('permissions:credential_index')


@permission_required('permissions.change_credential')
@login_required
def deactivate_credential(request, access_key):
    credential = get_object_or_404(models.Credential,
                                   creator=request.user,
                                   access_key=access_key)
    credential.deactivated = now()
    credential.save()
    return redirect('permissions:credential_index')
