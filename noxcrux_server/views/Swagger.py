from drf_spectacular.views import SpectacularSwaggerView
from csp.decorators import csp_update


class APIDocView(SpectacularSwaggerView):
    template_name = 'swagger_ui.html'

    @csp_update(SCRIPT_SRC="'unsafe-inline'")
    def get(self, request, *args, **kwargs):
        return super(APIDocView, self).get(self.request, *self.args, **self.kwargs)
