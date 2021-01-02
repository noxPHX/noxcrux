from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from noxcrux_server.views.LoginRequired import LoginRequiredView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from noxcrux_server.forms.Login import LoginForm, RegisterForm
from noxcrux_api.views.User import UserList


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            messages.success(self.request, 'Logged in successfully!')
            return super(LoginView, self).form_valid(form)
        else:
            messages.error(self.request, 'Incorrect credentials')
            return super(LoginView, self).get(self.request, *self.args, **self.kwargs)


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.request.data = form.cleaned_data
        res = UserList().post(self.request)
        if res.status_code == 201:
            messages.success(self.request, 'Account created successfully!')
            return super(RegisterView, self).form_valid(form)
        else:
            messages.error(self.request, 'Could not register your account')
            return super(RegisterView, self).get(self.request, *self.args, **self.kwargs)


class LogoutView(LoginRequiredView):

    def get(self, request, **kwargs):
        logout(request)
        messages.success(request, 'Logged out successfully!')
        return HttpResponseRedirect(reverse('login'))
