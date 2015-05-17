from django import forms

from localshop.apps.permissions import models


class TeamFormMixin(object):
    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop('team')
        super(TeamFormMixin, self).__init__(*args, **kwargs)


class TeamMemberAddForm(TeamFormMixin, forms.ModelForm):
    class Meta:
        model = models.TeamMember
        fields = ['user', 'role']

    def clean_user(self):
        user = self.cleaned_data['user']
        if user and self.team.members.filter(user=user).exists():
            raise forms.ValidationError(
                "%s is already a member of the team" % user.username)
        return user

    def save(self, commit=True):
        instance = super(TeamMemberAddForm, self).save(commit=False)
        if commit:
            instance.team = self.team
            instance.save()
        return instance


class TeamMemberRemoveForm(TeamFormMixin, forms.Form):
    member_obj = forms.ModelChoiceField(models.TeamMember.objects.all())

    def __init__(self, *args, **kwargs):
        super(TeamMemberRemoveForm, self).__init__(*args, **kwargs)
        self.fields['member_obj'] = forms.ModelChoiceField(
            self.team.members.all())

    def clean(self):
        member_obj = self.cleaned_data['member_obj']

        # This should never happen
        if member_obj.team.pk != self.team.pk:
            raise forms.ValidationError("Member is not part of the team")

        return self.cleaned_data
