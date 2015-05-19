from braces.views import LoginRequiredMixin, UserFormKwargsMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from localshop.apps.accounts import forms, models


class TeamListView(LoginRequiredMixin, generic.ListView):
    queryset = models.Team.objects.all()


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Team
    fields = ['description', 'name']
    template_name = 'accounts/team_form.html'

    def form_valid(self, form):
        team = form.save()
        team.members.create(user=self.request.user, role='owner')
        return super(TeamCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'accounts:team_detail', kwargs={'pk': self.object.pk})


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Team

    def get_context_data(self, *args, **kwargs):
        ctx = super(TeamDetailView, self).get_context_data(*args, **kwargs)
        ctx.update({
            'form_member_add': forms.TeamMemberAddForm(team=self.object),
        })
        return ctx


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Team
    fields = ['description', 'name']
    template_name = 'accounts/team_form.html'

    def get_success_url(self):
        return reverse(
            'accounts:team_detail', kwargs={'pk': self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Team

    def get_success_url(self):
        return reverse('accounts:team_list')


class TeamMixin(object):
    def dispatch(self, request, pk):
        self.team = get_object_or_404(models.Team, pk=pk)
        return super(TeamMixin, self).dispatch(request, pk)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(TeamMixin, self).get_form_kwargs(*args, **kwargs)
        kwargs['team'] = self.team
        return kwargs


class TeamMemberAddView(LoginRequiredMixin, TeamMixin, generic.FormView):
    http_method_names = ['post']
    form_class = forms.TeamMemberAddForm

    def form_valid(self, form):
        form.save()
        return redirect('accounts:team_detail', pk=self.team.pk)

    def form_invalid(self, form):
        return redirect('accounts:team_detail', pk=self.team.pk)


class TeamMemberRemoveView(LoginRequiredMixin, TeamMixin, generic.FormView):
    http_method_names = ['post']
    form_class = forms.TeamMemberRemoveForm

    def form_valid(self, form):
        form.cleaned_data['member_obj'].delete()
        return redirect('accounts:team_detail', pk=self.team.pk)

    def form_invalid(self, form):
        return redirect('accounts:team_detail', pk=self.team.pk)


class ProfileView(LoginRequiredMixin, generic.FormView):
    form_class = forms.ProfileForm
    template_name = 'accounts/profile.html'

    def form_valid(self, form):
        form.save()
        return super(ProfileView, self).form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProfileView, self).get_form_kwargs(*args, **kwargs)
        kwargs['instance'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('accounts:profile')


class AccessKeyListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'access_keys'

    def get_queryset(self):
        return self.request.user.access_keys.all()


class AccessKeyCreateView(LoginRequiredMixin, UserFormKwargsMixin,
                          generic.CreateView):
    template_name = 'accounts/accesskey_form.html'
    form_class = forms.AccessKeyForm


    def form_valid(self, form):
        form.save()
        return super(AccessKeyCreateView, self).form_valid(form)

    def get_queryset(self):
        return self.request.user.access_keys.all()

    def get_success_url(self):
        return reverse('accounts:access_key_list')


class AccessKeySecretView(LoginRequiredMixin, generic.DetailView):

    def get_queryset(self):
        return self.request.user.access_keys.all()

    def get(self, request, pk):
        if not request.is_ajax():
            raise SuspiciousOperation
        key = get_object_or_404(self.request.user.access_keys, pk=pk)
        return HttpResponse(key.secret_key)


class AccessKeyUpdateView(LoginRequiredMixin, UserFormKwargsMixin,
                          generic.UpdateView):
    template_name = 'accounts/accesskey_form.html'
    form_class = forms.AccessKeyForm


    def form_valid(self, form):
        form.save()
        return super(AccessKeyUpdateView, self).form_valid(form)

    def get_queryset(self):
        return self.request.user.access_keys.all()

    def get_success_url(self):
        return reverse('accounts:access_key_list')


class AccessKeyDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'accounts/accesskey_confirm_delete.html'
    context_object_name = 'access_key'

    def get_queryset(self):
        return self.request.user.access_keys.all()

    def get_success_url(self):
        return reverse('accounts:access_key_list')
