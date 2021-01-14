from noxcrux_server.mixins.Authenticated import LoginRequiredView, LoginRequiredFormView
from django.http import HttpResponseRedirect
from noxcrux_api.views.Horcrux import HorcruxDetail, HorcruxList
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from noxcrux_server.forms.Horcrux import HorcruxForm


class HorcruxAdd(LoginRequiredFormView):
    template_name = 'horcrux_add.html'
    form_class = HorcruxForm
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super(HorcruxAdd, self).get_initial()
        initial.update({'site': 'https://'})
        return initial

    def get_form_kwargs(self):
        kwargs = super(HorcruxAdd, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.request.data = form.cleaned_data
        res = HorcruxList().post(self.request)
        if res.status_code == 201:
            messages.success(self.request, 'Horcrux created successfully!')
            return super(HorcruxAdd, self).form_valid(form)
        else:
            messages.error(self.request, 'An error occurred')
            return super(HorcruxAdd, self).get(self.request, *self.args, **self.kwargs)


class HorcruxEdit(LoginRequiredFormView):
    template_name = 'horcrux_edit.html'
    form_class = HorcruxForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(HorcruxEdit, self).get_form_kwargs()
        horcrux = HorcruxDetail().get_object(self.kwargs['name'], self.request.user)
        kwargs.update({'instance': horcrux, 'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.request.data = form.cleaned_data
        res = HorcruxDetail().put(self.request, self.kwargs['name'])
        if res.status_code == 200:
            messages.success(self.request, 'Horcrux updated successfully!')
            return super(HorcruxEdit, self).form_valid(form)
        else:
            messages.error(self.request, 'An error occurred')
            return super(HorcruxEdit, self).get(self.request, *self.args, **self.kwargs)


class HorcruxDelete(LoginRequiredView):

    def get(self, request, *args, **kwargs):
        name = kwargs['name']
        res = HorcruxDetail().delete(request, name)
        if res.status_code == 204:
            messages.success(request, '%s removed successfully!' % name)
        else:
            messages.error(request, 'An error occurred')
        return HttpResponseRedirect(reverse('home'))
