#from auth_remember import remember_user
from django.template.response import TemplateResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, CreateView
from django.views.generic import UpdateView, DetailView, DeleteView

from localshop.utils import clean_redirect_url
from localshop.utils import permission_required
from localshop.permissions import models
from localshop.permissions.forms import LoginForm, UserForm


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


@permission_required('auth.add_user')
class UserListView(ListView):
    model = User
    template_name = 'permissions/user_list.html'


@permission_required('auth.change_user')
class UserDetailView(DetailView):
    model = User
    template_name = 'permissions/user_detail.html'


@permission_required('auth.add_user')
class UserCreateView(CreateView):
    form_class = UserForm
    model = User
    template_name = 'permissions/user_new.html'


@permission_required('auth.change_user')
class UserUpdateView(UpdateView):
    form_class = UserForm
    model = User
    template_name = 'permissions/user_edit.html'

    def get_success_url(self):
        return reverse('permissions:user_index')


@permission_required('permissions.add_permission')
class CidrListView(ListView):
    model = models.CIDR
    object_context_name = 'cidrs'


@permission_required('permissions.add_permission')
class CidrCreateView(CreateView):
    model = models.CIDR

    def get_success_url(self):
        return reverse('permissions:cidr_index')


@permission_required('permissions.change_permission')
class CidrUpdateView(UpdateView):
    model = models.CIDR

    def get_success_url(self):
        return reverse('permissions:cidr_index')


@permission_required('permissions.delete_permission')
class CidrDeleteView(DeleteView):
    model = models.CIDR

    def get_success_url(self):
        return reverse('permissions:cidr_index')
