from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredView(LoginRequiredMixin, View):
    """"""


class LoginRequiredTemplateView(LoginRequiredMixin, TemplateView):
    """"""
