from django import forms
from django.contrib.auth.models import User
from . import models

ERROR_MESSAGE_EMAIL = "Email error"
ERROR_MESSAGE_USER = "Username error"
ERROR_MESSAGE_PASSWORD = "Password error"


class CreateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    email = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class RestorePasswordForm(forms.ModelForm):
    email = forms.CharField(max_length=50)

    class Meta:
        model = models.RestorePasswordRequest
        fields = ('email',)


class ResetcodePasswordForm(forms.ModelForm):
    resetcode = forms.CharField(max_length=6)

    class Meta:
        model = models.RestorePasswordRequest
        fields = ('resetcode',)
