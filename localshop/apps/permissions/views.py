from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views import generic

from localshop.apps.permissions import forms, models


class TeamListView(LoginRequiredMixin, generic.ListView):
    queryset = models.Team.objects.all()


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Team
    fields = ['description', 'name']
    template_name = 'permissions/team_form.html'

    def form_valid(self, form):
        team = form.save()
        team.members.create(user=self.request.user, role='owner')
        return super(TeamCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'permissions:team_detail', kwargs={'pk': self.object.pk})


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
    template_name = 'permissions/team_form.html'

    def get_success_url(self):
        return reverse(
            'permissions:team_detail', kwargs={'pk': self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Team

    def get_success_url(self):
        return reverse('permissions:team_list')


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
        return redirect('permissions:team_detail', pk=self.team.pk)

    def form_invalid(self, form):
        return redirect('permissions:team_detail', pk=self.team.pk)


class TeamMemberRemoveView(LoginRequiredMixin, TeamMixin, generic.FormView):
    http_method_names = ['post']
    form_class = forms.TeamMemberRemoveForm

    def form_valid(self, form):
        form.cleaned_data['member_obj'].delete()
        return redirect('permissions:team_detail', pk=self.team.pk)

    def form_invalid(self, form):
        return redirect('permissions:team_detail', pk=self.team.pk)
