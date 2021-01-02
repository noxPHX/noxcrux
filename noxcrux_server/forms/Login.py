from django import forms
from django.contrib.auth.models import User


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
