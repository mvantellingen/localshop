from django import forms

from localshop.apps.packages import models


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
        obj.save()
        return obj


class ReleaseForm(forms.ModelForm):

    class Meta:
        model = models.Release
        fields = [
            'author', 'author_email', 'description', 'download_url',
            'home_page', 'license', 'metadata_version', 'summary', 'version',
        ]

    def clean_download_url(self):
        value = self.cleaned_data.get('value')
        if value is None:
            return ''
        return value


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
