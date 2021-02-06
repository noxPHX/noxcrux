from noxcrux_server.mixins.Authenticated import LoginRequiredListView
from noxcrux_api.views.Horcrux import HorcruxList


class HomeView(LoginRequiredListView):
    template_name = 'home.html'
    context_object_name = 'horcruxes'

    def get_queryset(self):
        return HorcruxList().get(self.request).data
