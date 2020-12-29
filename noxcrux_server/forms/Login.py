from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=255, required=True, label="",
                               widget=forms.TextInput(attrs={'class': "form-control my-1", 'placeholder': "username"}))
    password = forms.CharField(min_length=10, max_length=255, required=True, label="",
                               widget=forms.PasswordInput(attrs={'class': "form-control my-1", 'placeholder': "password"}))
