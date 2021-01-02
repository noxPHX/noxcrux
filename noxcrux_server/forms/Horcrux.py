from django import forms
from noxcrux_api.models.Horcrux import Horcrux


class HorcruxForm(forms.ModelForm):
    class Meta:
        model = Horcrux
        fields = ['name', 'horcrux', 'site']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user") if 'user' in kwargs else None
        super(HorcruxForm, self).__init__(*args, **kwargs)

    name = forms.CharField(max_length=255, required=True, label="",
                           widget=forms.TextInput(attrs={'class': "form-control my-1", 'placeholder': "Name"}))
    horcrux = forms.CharField(max_length=255, required=True, label="",
                              widget=forms.TextInput(attrs={'class': "form-control my-1", 'placeholder': "Horcrux"}))
    site = forms.CharField(max_length=255, required=True, label="",
                           widget=forms.TextInput(attrs={'class': "form-control my-1", 'placeholder': "Site"}))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Horcrux.objects.filter(name=name, owner=self.user).exclude(id=self.instance.id):
            raise forms.ValidationError("Horcrux with this name already exists!")
        return name
