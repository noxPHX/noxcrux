from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect
from noxcrux_api.views.Horcrux import HorcruxDetail, HorcruxList
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from noxcrux_server.forms.Horcrux import HorcruxForm


class HorcruxAdd(TemplateView):
    template_name = 'horcrux_add.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': HorcruxForm(initial={'site': 'https://'})})

    def post(self, request, **kwargs):
        form = HorcruxForm(request.POST)

        if form.is_valid():
            request.data = form.cleaned_data
            res = HorcruxList().post(request)
            if res.status_code == 201:
                messages.success(request, 'Horcrux created successfully!')
                return HttpResponseRedirect(reverse('home'))

        messages.error(request, 'An error occurred')
        return render(request, self.template_name, {'form': form})


class HorcruxEdit(TemplateView):
    template_name = 'horcrux_edit.html'

    def get(self, request, *args, **kwargs):
        horcrux = HorcruxDetail().get_object(kwargs['name'], request.user)
        form = HorcruxForm(instance=horcrux)
        return render(request, self.template_name, {'form': form, 'name': kwargs['name']})

    def post(self, request, **kwargs):
        horcrux = HorcruxDetail().get_object(kwargs['name'], request.user)
        form = HorcruxForm(request.POST, instance=horcrux)

        if form.is_valid():
            request.data = form.cleaned_data
            res = HorcruxDetail().put(request, kwargs['name'])
            if res.status_code == 200:
                messages.success(request, 'Horcrux updated successfully!')
                return HttpResponseRedirect(reverse('home'))

        messages.error(request, 'An error occurred')
        return render(request, self.template_name, {'form': form, 'name': kwargs['name']})


class HorcruxDelete(View):

    def get(self, request, *args, **kwargs):
        name = kwargs['name']
        res = HorcruxDetail().delete(request, name)
        if res.status_code == 204:
            messages.success(request, '%s removed successfully!' % name)
        else:
            messages.error(request, 'An error occurred')
        return HttpResponseRedirect(reverse('home'))
