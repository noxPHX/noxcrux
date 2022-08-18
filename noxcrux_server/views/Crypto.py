from django.views.generic import TemplateView


class CryptoView(TemplateView):
    template_name = 'crypto.html'
