from django import forms

from localshop.packages import models


class ReleaseForm(forms.ModelForm):
    class Meta:
        model = models.Release
        exclude = ['classifiers', 'package']


class ReleaseFileForm(forms.ModelForm):
    class Meta:
        model = models.ReleaseFile
        exclude = ['size', 'release', 'filename']

    def __init__(self, *args, **kwargs):
        super(ReleaseFileForm, self).__init__(*args, **kwargs)
        self.fields['pyversion'] = self.fields.pop('python_version')
        self.fields['pyversion'].required = False

    def save(self, commit=True):
        obj = super(ReleaseFileForm, self).save(False)
        obj.python_version = self.cleaned_data['pyversion'] or 'source'
        if commit:
            obj.save()
        return obj
