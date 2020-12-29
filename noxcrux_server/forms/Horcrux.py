from django import forms
from noxcrux_api.models.Horcrux import Horcrux


class HorcruxForm(forms.ModelForm):
    class Meta:
        model = Horcrux
        fields = ['name', 'horcrux', 'site']

    name = forms.CharField(max_length=255, required=True, label="",
                           widget=forms.TextInput(attrs={'class': "form-control my-1", 'placeholder': "Name"}))
    horcrux = forms.CharField(max_length=255, required=True, label="",
                              widget=forms.TextInput(attrs={'class': "form-control my-1", 'placeholder': "Horcrux"}))
    site = forms.CharField(max_length=255, required=True, label="",
                           widget=forms.TextInput(attrs={'class': "form-control my-1", 'placeholder': "Site"}))
