from django.contrib.auth import login
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from noxcrux_server.forms.User import OTPForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from noxcrux_server.mixins.Authenticated import LoginRequiredTemplateView, LoginRequiredFormView
from django.shortcuts import render
from noxcrux_api.views.OTP import get_user_totp_device, TOTPView


class TOTPLoginView(FormView):
    template_name = 'totp.html'
    form_class = OTPForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.session.get('username'):
            return HttpResponseRedirect(reverse('login'))
        return super(TOTPLoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TOTPLoginView, self).get_form_kwargs()
        kwargs['user'] = authenticate(username=self.request.session.get('username'), password=self.request.session.get('password'))
        self.kwargs['user'] = kwargs['user']
        return kwargs

    def form_valid(self, form):
        del self.request.session['username']
        del self.request.session['password']
        login(self.request, self.kwargs['user'])
        messages.success(self.request, 'Logged in successfully!')
        return super(TOTPLoginView, self).form_valid(form)


class TOTPMainView(LoginRequiredTemplateView):
    template_name = '2FA.html'

    def get(self, request, *args, **kwargs):
        context = {}
        device = get_user_totp_device(request.user)
        if device:
            context['device'] = device
        return render(request, self.template_name, context)


class TOTPSecretView(LoginRequiredTemplateView):
    template_name = '2FA_secret.html'

    def get(self, request, *args, **kwargs):
        res = TOTPView().get(request)
        context = {
            'url': res.data,
        }
        device = get_user_totp_device(request.user)
        if device:
            context['device'] = device
        return render(request, self.template_name, context)


class TOTPConfirmView(LoginRequiredFormView):
    template_name = '2FA_confirm.html'
    form_class = OTPForm
    success_url = reverse_lazy('2FA')

    def dispatch(self, request, *args, **kwargs):
        if get_user_totp_device(request.user, confirmed=True):
            return HttpResponseRedirect(self.success_url)
        return super(TOTPConfirmView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TOTPConfirmView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user, 'verify': False})
        return kwargs

    def form_valid(self, form):
        res = TOTPView().post(self.request, form.cleaned_data['totp_code'])
        if res.status_code == 200:
            messages.success(self.request, '2FA confirmed successfully!')
            return super(TOTPConfirmView, self).form_valid(form)
        else:
            messages.error(self.request, 'An error occurred')
            return super(TOTPConfirmView, self).get(self.request, *self.args, **self.kwargs)
