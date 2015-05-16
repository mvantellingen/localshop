from django import forms

from localshop.apps.permissions.models import CIDR, Team


class RepositoryFormMixin(object):
    def __init__(self, *args, **kwargs):
        self.repository = kwargs.pop('repository')
        super(RepositoryFormMixin, self).__init__(*args, **kwargs)


class AccessControlForm(RepositoryFormMixin, forms.ModelForm):

    class Meta:
        fields = ['label', 'cidr', 'require_credentials']
        model = CIDR

    def save(self):
        instance = super(AccessControlForm, self).save(commit=False)
        instance.repository = self.repository
        instance.save()
        return instance


class RepositoryTeamForm(RepositoryFormMixin, forms.Form):
    delete = forms.BooleanField(widget=forms.HiddenInput, required=False)
    team = forms.ModelChoiceField(Team.objects.all())

    def __init__(self, *args, **kwargs):
        super(RepositoryTeamForm, self).__init__(*args, **kwargs)

        if not self.data:
            self.fields['team'].queryset = (
                self.fields['team'].queryset
                .exclude(
                    pk__in=self.repository.teams.values_list('pk', flat=True)))

    def save(self):
        if self.cleaned_data['delete']:
            self.repository.teams.remove(self.cleaned_data['team'])
        else:
            self.repository.teams.add(self.cleaned_data['team'])
