from drf_spectacular.views import SpectacularSwaggerView


class APIDocView(SpectacularSwaggerView):
    template_name = 'swagger_ui.html'
