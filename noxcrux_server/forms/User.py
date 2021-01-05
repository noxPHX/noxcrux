from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': "form-control my-1", 'placeholder': "username"})
        self.fields['username'].label = ""
        self.fields['password'].widget.attrs.update({'class': "form-control my-1", 'placeholder': "password"})
        self.fields['password'].label = ""


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': "form-control my-1", 'placeholder': "username"})
        self.fields['username'].help_text = ""
        self.fields['username'].label = ""
        self.fields['password1'].widget.attrs.update({'class': "form-control my-1", 'placeholder': "password"})
        self.fields['password1'].help_text = ""
        self.fields['password1'].label = ""
        self.fields['password2'].widget.attrs.update({'class': "form-control my-1", 'placeholder': "confirm password"})
        self.fields['password2'].help_text = ""
        self.fields['password2'].label = ""


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


class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    username = forms.CharField(max_length=255, required=True, label="",
                               widget=forms.TextInput(attrs={'class': "form-control my-1", 'placeholder': "new username"}))
