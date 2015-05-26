import operator

from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils.text import ugettext_lazy as _
from django.views import generic
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin

from localshop.apps.dashboard import forms
from localshop.apps.packages import models
from localshop.apps.packages.tasks import fetch_package


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self):
        return {
            'repositories': self.repositories,
        }

    @property
    def repositories(self):
        user = self.request.user

        if user.is_superuser:
            return models.Repository.objects.all()

        repositories = set()
        for team_membership in user.team_memberships.all():
            for repository in team_membership.team.repositories.all():
                repositories.add(repository)
        return sorted(repositories, key=operator.attrgetter('name'))


class RepositoryCreateView(SuperuserRequiredMixin, generic.CreateView):
    form_class = forms.RepositoryForm
    template_name = 'dashboard/repository_create.html'

    def get_success_url(self):
        return reverse(
            'dashboard:repository_detail', kwargs={'slug': self.object.slug})


class RepositoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Repository
    template_name = 'dashboard/repository_detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(RepositoryDetailView, self).get_context_data(
            *args, **kwargs)

        ctx.update({
            'simple_index_url': self.request.build_absolute_uri(
                self.object.simple_index_url),
        })
        return ctx

    @property
    def repository(self):
        return self.object


class RepositoryMixin(object):
    require_role = None
    repository_slug_name = 'repo'

    def dispatch(self, request, *args, **kwargs):
        self.repository = get_object_or_404(
            models.Repository.objects, slug=kwargs[self.repository_slug_name])

        if self.require_role:
            if not self.repository.check_user_role(
                request.user, self.require_role
            ):
                return HttpResponseForbidden('No access')

        return super(RepositoryMixin, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RepositoryMixin, self).get_form_kwargs(*args, **kwargs)
        kwargs['repository'] = self.repository
        return kwargs


class RepositorySettingsMixin(RepositoryMixin, LoginRequiredMixin):
    require_role = ['owner']



class RepositoryUpdateView(RepositorySettingsMixin, generic.UpdateView):
    model = models.Repository
    context_object_name = 'repository'
    form_class = forms.RepositoryForm
    repository_slug_name = 'slug'
    template_name = 'dashboard/repository_settings/edit.html'

    def get_success_url(self):
        return reverse(
            'dashboard:repository_detail', kwargs={'slug': self.object.slug})

    def get_object(self):
        return self.repository

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RepositoryUpdateView, self).get_form_kwargs(
            *args, **kwargs)
        del kwargs['repository']
        return kwargs


class RepositoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Repository
    template_name = 'dashboard/repository_settings/delete.html'

    def get_success_url(self):
        return reverse('dashboard:index')

    @property
    def repository(self):
        return self.object


class PackageAddView(RepositoryMixin, LoginRequiredMixin, generic.FormView):
    form_class = forms.PackageAddForm

    def form_valid(self, form):
        package_name = form.cleaned_data['name']
        messages.info(
            self.request,
            _("Retrieving package information from '%s'" % form.cleaned_data['name']))
        fetch_package.delay(self.repository.pk, package_name)

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, _("Invalid package name"))
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            'dashboard:repository_detail', kwargs={
                'slug': self.repository.slug
        })


class PackageDetail(RepositoryMixin, LoginRequiredMixin, generic.DetailView):
    require_role = ['developer', 'owner']
    context_object_name = 'package'
    slug_url_kwarg = 'name'
    slug_field = 'name'
    template_name = 'dashboard/package_detail.html'

    def get_queryset(self):
        return self.repository.packages.all()

    def get_context_data(self, *args, **kwargs):
        context = super(PackageDetail, self).get_context_data(*args, **kwargs)
        context['release'] = self.object.last_release
        return context


class CidrListView(RepositorySettingsMixin, generic.ListView):
    object_context_name = 'cidrs'
    template_name = 'dashboard/repository_settings/cidr_list.html'

    def get_queryset(self):
        return self.repository.cidr_list.all()


class CidrCreateView(RepositorySettingsMixin, generic.CreateView):
    form_class = forms.AccessControlForm
    template_name = 'dashboard/repository_settings/cidr_form.html'

    def get_success_url(self):
        return reverse('dashboard:repo_settings:cidr_index', kwargs={
            'repo': self.repository.slug,
        })

    def get_queryset(self):
        return self.repository.cidr_list.all()


class CidrUpdateView(RepositorySettingsMixin, generic.UpdateView):
    form_class = forms.AccessControlForm
    template_name = 'dashboard/repository_settings/cidr_form.html'

    def get_success_url(self):
        return reverse('dashboard:repo_settings:cidr_index', kwargs={
            'repo': self.repository.slug,
        })

    def get_queryset(self):
        return self.repository.cidr_list.all()


class CidrDeleteView(RepositorySettingsMixin, generic.DeleteView):
    form_class = forms.AccessControlForm
    template_name = 'dashboard/repository_settings/cidr_confirm_delete.html'

    def get_success_url(self):
        return reverse('dashboard:repo_settings:cidr_index', kwargs={
            'repo': self.repository.slug,
        })

    def get_queryset(self):
        return self.repository.cidr_list.all()


class CredentialListView(RepositorySettingsMixin, generic.ListView):
    object_context_name = 'credentials'
    template_name = 'dashboard/repository_settings/credential_list.html'

    def get_queryset(self):
        return self.repository.credentials.all()

    def get_context_data(self, **kwargs):
        context = super(CredentialListView, self).get_context_data(**kwargs)
        context['current_url'] = Site.objects.get_current()
        return context


class CredentialCreateView(RepositorySettingsMixin, generic.CreateView):
    form_class = forms.CredentialModelForm
    template_name = 'dashboard/repository_settings/credential_form.html'

    def get_queryset(self):
        return self.repository.credentials.all()

    def get_success_url(self):
        return reverse('dashboard:repo_settings:credential_index', kwargs={
            'repo': self.repository.slug,
        })


class CredentialSecretKeyView(RepositorySettingsMixin, generic.View):

    def get(self, request, repo, access_key):
        if not request.is_ajax():
            raise SuspiciousOperation
        credential = get_object_or_404(
            self.repository.credentials, access_key=access_key)
        return HttpResponse(credential.secret_key)


class CredentialUpdateView(RepositorySettingsMixin, generic.UpdateView):
    form_class = forms.CredentialModelForm
    slug_field = 'access_key'
    slug_url_kwarg = 'access_key'
    template_name = 'dashboard/repository_settings/credential_form.html'

    def get_queryset(self):
        return self.repository.credentials.all()

    def get_success_url(self):
        return reverse('dashboard:repo_settings:credential_index', kwargs={
            'repo': self.repository.slug,
        })


class CredentialDeleteView(RepositorySettingsMixin, generic.DeleteView):
    slug_field = 'access_key'
    slug_url_kwarg = 'access_key'

    def get_success_url(self):
        return reverse('dashboard:repo_settings:credential_index', kwargs={
            'repo': self.repository.slug,
        })


class TeamAccessView(RepositorySettingsMixin, generic.FormView):
    form_class = forms.RepositoryTeamForm
    template_name = 'dashboard/repository_settings/teams.html'

    def get_success_url(self):
        return reverse('dashboard:repo_settings:team_access', kwargs={
            'repo': self.repository.slug,
        })

    def form_valid(self, form):
        form.save()
        return super(TeamAccessView, self).form_valid(form)
