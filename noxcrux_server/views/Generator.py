from noxcrux_server.mixins.Authenticated import LoginRequiredFormView
from noxcrux_api.views.Generator import GeneratorDetail
from django.urls import reverse_lazy
from django.contrib import messages
from noxcrux_server.forms.Generator import GeneratorForm


class Generator(LoginRequiredFormView):
    template_name = 'generator.html'
    form_class = GeneratorForm
    success_url = reverse_lazy('generator')

    def get_initial(self):
        initial = super(Generator, self).get_initial()
        generator = GeneratorDetail().get_generator(self.request.user)
        initial.update({'lower': True, 'generated': generator.generate()})
        return initial

    def get_form_kwargs(self):
        kwargs = super(Generator, self).get_form_kwargs()
        generator = GeneratorDetail().get_generator(self.request.user)
        kwargs.update({'instance': generator})
        return kwargs

    def form_valid(self, form):
        self.request.data = form.cleaned_data
        self.request.method = 'PUT'
        res = GeneratorDetail().as_view()(self.request)
        if res.status_code == 200:
            return super(Generator, self).form_valid(form)
        else:
            messages.error(self.request, 'An error occurred')
            return super(Generator, self).get(self.request, *self.args, **self.kwargs)
