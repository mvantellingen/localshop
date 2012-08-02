#from auth_remember import remember_user
from django.template.response import TemplateResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, CreateView
from django.views.generic import UpdateView, DetailView, DeleteView

from localshop.views import LoginRequiredMixin, PermissionRequiredMixin
from localshop.utils import clean_redirect_url
from localshop.apps.permissions import models
from localshop.apps.permissions.forms import LoginForm, UserForm


def login(request):
    """Authenticate the user and redirect to the path given in the `next`
    param.

    """
    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data

        user = auth.authenticate(
            username=data['username'], password=data['password'])

        if user:
            auth.login(request, user)
            #if data['remember_me']:
            #    remember_user(request, user)

            return redirect(
                clean_redirect_url(request, request.GET.get('next') or '/'))
        form.add_non_field_error(_("Invalid username/password"))

    return TemplateResponse(request, 'permissions/login.html', {
        'form': form,
        'user': request.user
    })


def logout(request):
    auth.logout(request)
    return redirect('permissions:login')


def permission_denied(request):
    """Return the view for permission denied errors.

    Note that this is a bit buggy, we need to render the template
    and return te content.

    """
    return TemplateResponse(request, '403.html').render()


def dashboard(request):
    return TemplateResponse(request, 'permissions/dashboard.html')


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'permissions/user_list.html'
    permission_required = 'auth.add_user'


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'permissions/user_detail.html'
    permission_required = 'auth.change_user'


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = UserForm
    model = User
    template_name = 'permissions/user_new.html'
    permission_required = 'auth.add_user'


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'permissions/user_edit.html'
    permission_required = 'auth.change_user'

    def get_success_url(self):
        return reverse('permissions:user_index')


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
    credential.deactivated = models.now()
    credential.save()
    return redirect('permissions:credential_index')
