from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.urls import reverse
from django.contrib import messages
from noxcrux_server.forms.Login import LoginForm


class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return HttpResponseRedirect(reverse('home'))

        messages.error(request, 'Incorrect credentials')
        return render(request, self.template_name, {'form': form})


#class RegisterView(TemplateView):
#    template_name = 'register.html'


class LogoutView(View):

    def get(self, request, **kwargs):
        logout(request)
        messages.success(request, 'Logged out successfully!')
        return HttpResponseRedirect(reverse('login'))
