from django.views.generic import TemplateView
from django.shortcuts import render
from noxcrux_api.views.Horcrux import HorcruxList


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        res = HorcruxList().get(request)
        context = {
            'horcruxes': res.data,
        }
        return render(request, self.template_name, context)
