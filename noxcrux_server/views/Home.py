from noxcrux_server.mixins.Authenticated import LoginRequiredListView
from noxcrux_api.views.Horcrux import HorcruxList, HorcruxGrantedList


class HomeView(LoginRequiredListView):
    template_name = 'home.html'
    context_object_name = 'horcruxes'

    def get_queryset(self):
        horcruxes = {
            'mines': HorcruxList().get(self.request).data,
            'shared': HorcruxGrantedList().get(self.request).data
        }
        return horcruxes
