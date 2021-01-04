from noxcrux_server.views.LoginRequired import LoginRequiredFormView, LoginRequiredTemplateView
from noxcrux_server.forms.Login import UsernameForm
from django.urls import reverse_lazy
from noxcrux_api.views.User import UserUpdate
from django.contrib import messages


class ProfileView(LoginRequiredTemplateView):
    template_name = 'profile.html'


class UsernameUpdateView(LoginRequiredFormView):
    template_name = 'edit_username.html'
    form_class = UsernameForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        self.request.data = form.cleaned_data
        res = UserUpdate().put(self.request, self.request.user.username)
        if res.status_code == 200:
            messages.success(self.request, 'Username updated successfully!')
            return super(UsernameUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'An error occurred')
            return super(UsernameUpdateView, self).get(self.request, *self.args, **self.kwargs)
