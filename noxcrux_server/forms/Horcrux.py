from django import forms
from noxcrux_api.models.Horcrux import Horcrux
from django.core.validators import RegexValidator, URLValidator
from noxcrux_api.models.Generator import ALLOWED_SYMBOLS
import re

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]+$', 'Only alphanumeric characters are allowed.')
horcrux_validator = RegexValidator(r'^[0-9a-zA-Z' + re.escape(ALLOWED_SYMBOLS) + ']+$', 'Only alphanumeric characters and ' + ALLOWED_SYMBOLS + ' symbols are allowed.')


class HorcruxForm(forms.ModelForm):
    class Meta:
        model = Horcrux
        fields = ['name', 'horcrux', 'site']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user") if 'user' in kwargs else None
        super(HorcruxForm, self).__init__(*args, **kwargs)

    name = forms.CharField(max_length=255, required=True, label="Name", validators=[alphanumeric])
    horcrux = forms.CharField(max_length=255, required=True, label="Horcrux", validators=[horcrux_validator])
    site = forms.CharField(max_length=255, required=True, label="Site", validators=[URLValidator()])

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Horcrux.objects.filter(name=name, owner=self.user).exclude(id=self.instance.id):
            raise forms.ValidationError("Horcrux with this name already exists!")
        return name
