from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views import generic

from localshop.apps.dashboard import forms
from localshop.apps.packages import models
from localshop.views import LoginRequiredMixin, PermissionRequiredMixin


class IndexView(generic.TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self):

        recent_local = (
            models.Release.objects
            .filter(package__is_local=True)
            .order_by('-created')
            .all()[:5])

        recent_mirror = (
            models.ReleaseFile.objects
            .filter(release__package__is_local=False)
            .exclude(distribution='')
            .order_by('-modified')
            .all()[:10])

        return {
            'recent_local': recent_local,
            'recent_mirror': recent_mirror,
        }


class RepositoryListView(LoginRequiredMixin, generic.ListView):
    queryset = models.Repository.objects.all()
    template_name = 'dashboard/repository_list.html'
    context_object_name = 'repositories'


class RepositoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Repository
    fields = ['name', 'slug', 'description']
    template_name = 'dashboard/repository_form.html'

    def get_success_url(self):
        return reverse(
            'dashboard:repository_detail', kwargs={'pk': self.object.pk})


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


class RepositoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Repository
    fields = ['name', 'slug', 'description']
    template_name = 'dashboard/repository_form.html'

    def get_success_url(self):
        return reverse(
            'dashboard:repository_detail', kwargs={'slug': self.object.slug})


class RepositoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Repository

    def get_success_url(self):
        return reverse(
            'dashboard:repository_detail', kwargs={'slug': self.object.slug})


class RepositoryMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.repository = get_object_or_404(
            models.Repository.objects, slug=kwargs['repo'])
        return super(RepositoryMixin, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RepositoryMixin, self).get_form_kwargs(*args, **kwargs)
        kwargs['repository'] = self.repository
        return kwargs


class RepositorySettingsMixin(RepositoryMixin, LoginRequiredMixin,
                              PermissionRequiredMixin):
    pass



class PackageDetail(RepositoryMixin, LoginRequiredMixin,
                    PermissionRequiredMixin, generic.DetailView):
    context_object_name = 'package'
    slug_url_kwarg = 'name'
    slug_field = 'name'
    permission_required = 'packages.view_package'
    template_name = 'dashboard/package_detail.html'

    def get_queryset(self):
        return self.repository.packages.all()

    def get_context_data(self, *args, **kwargs):
        context = super(PackageDetail, self).get_context_data(*args, **kwargs)
        context['release'] = self.object.last_release
        return context



class CidrListView(RepositorySettingsMixin, generic.ListView):
    object_context_name = 'cidrs'
    permission_required = 'permissions.view_cidr'
    template_name = 'dashboard/repository_settings/cidr_list.html'

    def get_queryset(self):
        return self.repository.cidr_list.all()


class CidrCreateView(RepositorySettingsMixin, generic.CreateView):
    permission_required = 'permissions.add_cidr'
    form_class = forms.AccessControlForm
    template_name = 'dashboard/repository_settings/cidr_form.html'

    def get_success_url(self):
        return reverse('dashboard:repo_settings_cidr_index', kwargs={
            'repo': self.repository.slug,
        })

    def get_queryset(self):
        return self.repository.cidr_list.all()


class CidrUpdateView(RepositorySettingsMixin, generic.UpdateView):
    permission_required = 'permissions.change_cidr'
    form_class = forms.AccessControlForm
    template_name = 'dashboard/repository_settings/cidr_form.html'

    def get_success_url(self):
        return reverse('dashboard:repo_settings_cidr_index', kwargs={
            'repo': self.repository.slug,
        })

    def get_queryset(self):
        return self.repository.cidr_list.all()


class CidrDeleteView(RepositorySettingsMixin, generic.DeleteView):
    permission_required = 'permissions.delete_cidr'
    form_class = forms.AccessControlForm
    template_name = 'dashboard/repository_settings/cidr_confirm_delete.html'

    def get_success_url(self):
        return reverse('dashboard:repo_settings_cidr_index', kwargs={
            'repo': self.repository.slug,
        })

    def get_queryset(self):
        return self.repository.cidr_list.all()
