from django import forms

from localshop.apps.packages import models
from localshop.apps.packages.pypi import normalize_name


class PypiReleaseDataForm(forms.ModelForm):
    class Meta:
        model = models.Release
        fields = [
            'author', 'author_email', 'description', 'download_url',
            'home_page', 'license', 'summary', 'version',
        ]


class PackageForm(forms.ModelForm):
    class Meta:
        model = models.Package
        fields = [
            'name',
        ]

    def __init__(self, *args, **kwargs):
        self._repository = kwargs.pop('repository')
        super(PackageForm, self).__init__(*args, **kwargs)
        self.base_fields['name'].error_messages.update({
            'invalid': 'Enter a valid name consisting of letters, numbers, underscores or hyphens'
        })

    def save(self):
        obj = super(PackageForm, self).save(commit=False)
        obj.is_local = True
        obj.repository = self._repository
        obj.normalized_name = normalize_name(obj.name)
        obj.save()
        return obj


class ReleaseForm(forms.ModelForm):

    class Meta:
        model = models.Release
        fields = [
            'author', 'author_email', 'description', 'download_url',
            'home_page', 'license', 'metadata_version', 'summary', 'version',
        ]


class ReleaseFileForm(forms.ModelForm):
    class Meta:
        model = models.ReleaseFile
        fields = [
            'filetype', 'distribution', 'md5_digest', 'python_version',
            'url'
        ]

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
