from django.views.generic import View, TemplateView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredView(LoginRequiredMixin, View):
    ...


class LoginRequiredTemplateView(LoginRequiredMixin, TemplateView):
    ...


class LoginRequiredFormView(LoginRequiredMixin, FormView):
    ...


class LoginRequiredListView(LoginRequiredMixin, ListView):
    ...
