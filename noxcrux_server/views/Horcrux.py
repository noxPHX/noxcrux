from noxcrux_server.views.LoginRequired import LoginRequiredView, LoginRequiredTemplateView, LoginRequiredFormView
from django.http import HttpResponseRedirect
from noxcrux_api.views.Horcrux import HorcruxDetail, HorcruxList
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import render
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


class HorcruxEdit(LoginRequiredTemplateView):
    template_name = 'horcrux_edit.html'

    def get(self, request, *args, **kwargs):
        horcrux = HorcruxDetail().get_object(kwargs['name'], request.user)
        form = HorcruxForm(instance=horcrux)
        return render(request, self.template_name, {'form': form, 'name': kwargs['name']})

    def post(self, request, *args, **kwargs):
        horcrux = HorcruxDetail().get_object(kwargs['name'], request.user)
        form = HorcruxForm(request.POST, instance=horcrux, user=request.user)

        if form.is_valid():
            request.data = form.cleaned_data
            res = HorcruxDetail().put(request, kwargs['name'])
            if res.status_code == 200:
                messages.success(request, 'Horcrux updated successfully!')
                return HttpResponseRedirect(reverse('home'))

        messages.error(request, 'An error occurred')
        return render(request, self.template_name, {'form': form, 'name': kwargs['name']})


class HorcruxDelete(LoginRequiredView):

    def get(self, request, *args, **kwargs):
        name = kwargs['name']
        res = HorcruxDetail().delete(request, name)
        if res.status_code == 204:
            messages.success(request, '%s removed successfully!' % name)
        else:
            messages.error(request, 'An error occurred')
        return HttpResponseRedirect(reverse('home'))
