from django import forms
from django.contrib.auth.models import User
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _

from localshop.accounts import models


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        max_length=75)

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False)
    )

    remember_me = forms.BooleanField(label=_("Remember me"), required=False)

    def add_non_field_error(self, message):
        error_list = self.errors.setdefault(NON_FIELD_ERRORS, ErrorList())
        error_list.append(message)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']

