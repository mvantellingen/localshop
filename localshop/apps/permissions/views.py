from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.utils.timezone import now

from localshop.apps.permissions import models


class TeamListView(LoginRequiredMixin, generic.ListView):
    queryset = models.Team.objects.all()


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Team
    fields = ['description', 'name']
    template_name = 'permissions/team_form.html'

    def get_success_url(self):
        return reverse(
            'permissions:team_detail', kwargs={'pk': self.object.pk})


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Team


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
        return reverse(
            'permissions:team_detail', kwargs={'pk': self.object.pk})

