from noxcrux_server.mixins.Authenticated import LoginRequiredTemplateView
from django.shortcuts import render
from noxcrux_api.views.Horcrux import HorcruxList


class HomeView(LoginRequiredTemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        res = HorcruxList().get(request)
        context = {
            'horcruxes': res.data,
        }
        return render(request, self.template_name, context)
