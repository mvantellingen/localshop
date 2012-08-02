from django import forms

from localshop.apps.packages import models


class PypiReleaseDataForm(forms.ModelForm):
    class Meta:
        model = models.Release
        exclude = ['classifiers', 'package', 'user', 'metadata_version']


class ReleaseForm(forms.ModelForm):
    class Meta:
        model = models.Release
        exclude = ['classifiers', 'package', 'user']


class ReleaseFileForm(forms.ModelForm):
    class Meta:
        model = models.ReleaseFile
        exclude = ['size', 'release', 'filename', 'user']

    def __init__(self, *args, **kwargs):
        super(ReleaseFileForm, self).__init__(*args, **kwargs)
        self.fields['pyversion'] = self.fields.pop('python_version')
        self.fields['pyversion'].required = False

    def save(self, commit=True):
        obj = super(ReleaseFileForm, self).save(False)
        obj.python_version = self.cleaned_data['pyversion'] or 'n/a'
        if commit:
            obj.save()
        return obj
