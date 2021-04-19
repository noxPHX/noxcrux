from django import forms
from noxcrux_api.models.Generator import Generator
from noxcrux_api.models.Generator import ALLOWED_SYMBOLS


class GeneratorForm(forms.ModelForm):
    class Meta:
        model = Generator
        fields = ['lower', 'upper', 'numeric', 'symbol', 'size', 'generated']
        help_texts = {
            'upper': 'Upper case letters.',
            'numeric': 'Numeric characters.',
            'symbol': f'Special characters among {ALLOWED_SYMBOLS}'
        }

    lower = forms.BooleanField(required=False, disabled=True, help_text="Lower case letters, required.")
    generated = forms.CharField(label="Generated", required=False, disabled=True,
                                help_text="This is a generated value for you!")
