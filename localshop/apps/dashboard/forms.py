from django import forms

from localshop.apps.permissions.models import CIDR


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
