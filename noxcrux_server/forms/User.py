from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings


class RegisterForm(UserCreationForm):

    def clean(self):
        if settings.REGISTRATION_OPEN is False:
            raise forms.ValidationError('Registrations are closed.')
        return super(RegisterForm, self).clean()


class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    username = forms.CharField(max_length=255, required=True, label="New username")


class DeleteUserForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    password = forms.CharField(max_length=128, required=True, label="Confirm your password", widget=forms.PasswordInput())

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError("Your password was entered incorrectly. Please enter it again.", code='password_incorrect')
        return password
