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


class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['registration_open'] = settings.REGISTRATION_OPEN
        return context

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
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
        if settings.REGISTRATION_OPEN is False:
            messages.warning(request, 'Registrations are closed.')
            return HttpResponseRedirect(reverse('login'))

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.data = {
            'username': form.cleaned_data['username'],
            'password': form.cleaned_data['password1']
        }
        res = UserList().post(self.request)
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
