from noxcrux_server.mixins.Authenticated import LoginRequiredListView
from noxcrux_api.views.Horcrux import HorcruxList, HorcruxGrantedList, HorcruxSearch, HorcruxGrantedSearch


class HomeView(LoginRequiredListView):
    template_name = 'home.html'
    context_object_name = 'horcruxes'

    def get_queryset(self):
        if self.request.GET.get("search"):
            horcruxes = {
                'mines': HorcruxSearch().as_view()(self.request, search=self.request.GET.get("search")).data,
                'granted': HorcruxGrantedSearch().as_view()(self.request, search=self.request.GET.get("search")).data,
            }
        else:
            horcruxes = {
                'mines': HorcruxList().as_view()(self.request).data,
                'granted': HorcruxGrantedList().as_view()(self.request).data
            }
        return horcruxes
