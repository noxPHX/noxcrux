from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.Form):

    username = forms.CharField(max_length=255, required=True, label="",
                               widget=forms.TextInput(attrs={'class': "form-control my-1", 'placeholder': "username"}))
    password = forms.CharField(max_length=255, required=True, label="",
                               widget=forms.PasswordInput(
                                   attrs={'class': "form-control my-1", 'placeholder': "password"}))


class RegisterForm(forms.ModelForm, LoginForm):
    class Meta:
        model = User
        fields = ['username']

    confirm = forms.CharField(max_length=255, required=True, label="", widget=forms.PasswordInput(
        attrs={'class': "form-control my-1", 'placeholder': "confirm password"}))

    def clean_confirm(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm'):
            raise forms.ValidationError("Passwords does not match")
        return self.cleaned_data.get('confirm')


class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    username = forms.CharField(max_length=255, required=True, label="",
                               widget=forms.TextInput(attrs={'class': "form-control my-1", 'placeholder': "new username"}))


class PasswordUpdateForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': "form-control my-1", 'placeholder': "current password"})
        self.fields['old_password'].label = ""
        self.fields['new_password1'].widget.attrs.update({'class': "form-control my-1", 'placeholder': "new password"})
        self.fields['new_password1'].help_text = ""
        self.fields['new_password1'].label = ""
        self.fields['new_password2'].widget.attrs.update({'class': "form-control my-1", 'placeholder': "confirm new password"})
        self.fields['new_password2'].label = ""
