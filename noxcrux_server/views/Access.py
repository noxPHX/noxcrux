from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from noxcrux_server.mixins.Authenticated import LoginRequiredView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from noxcrux_server.forms.User import RegisterForm
from noxcrux_api.views.User import UserList
from django.conf import settings
from noxcrux_api.views.OTP import get_user_totp_device


class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['registration_open'] = settings.REGISTRATION_OPEN
        return context

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:

            device = get_user_totp_device(user, confirmed=True)
            if device:
                self.request.session['username'] = username
                self.request.session['password'] = password
                return HttpResponseRedirect(reverse('totp'))

            login(self.request, user)
            messages.success(self.request, 'Logged in successfully!')
            return super(LoginView, self).form_valid(form)
        else:
            messages.error(self.request, 'Could not log in')
            return super(LoginView, self).get(self.request, *self.args, **self.kwargs)


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        if settings.REGISTRATION_OPEN is False:
            messages.warning(request, 'Registrations are closed.')
            return HttpResponseRedirect(reverse('login'))

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        res = UserList().as_view()(self.request)
        if res.status_code == 201:
            messages.success(self.request, 'Account created successfully!')
            return super(RegisterView, self).form_valid(form)
        else:
            messages.error(self.request, 'Could not register your account')
            return super(RegisterView, self).get(self.request, *self.args, **self.kwargs)


class LogoutView(LoginRequiredView):

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Logged out successfully!')
        return HttpResponseRedirect(reverse('login'))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(LogoutView, self).dispatch(request, *args, **kwargs)
