from django.contrib.auth import login
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from noxcrux_server.forms.User import OTPForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse


class TOTPView(FormView):
    template_name = 'totp.html'
    form_class = OTPForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.session.get('username'):
            return HttpResponseRedirect(reverse('login'))
        return super(TOTPView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TOTPView, self).get_form_kwargs()
        kwargs['user'] = authenticate(username=self.request.session.get('username'), password=self.request.session.get('password'))
        self.kwargs['user'] = kwargs['user']
        return kwargs

    def form_valid(self, form):
        del self.request.session['username']
        del self.request.session['password']
        login(self.request, self.kwargs['user'])
        messages.success(self.request, 'Logged in successfully!')
        return super(TOTPView, self).form_valid(form)
