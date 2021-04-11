from noxcrux_server.mixins.Authenticated import LoginRequiredFormView, LoginRequiredTemplateView
from noxcrux_server.forms.User import UsernameForm, DeleteUserForm
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from noxcrux_api.views.User import PasswordUpdate, Profile
from django.contrib import messages


class ProfileView(LoginRequiredTemplateView):
    template_name = 'profile.html'


class UsernameUpdateView(LoginRequiredFormView):
    template_name = 'edit_username.html'
    form_class = UsernameForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        self.request.data = form.cleaned_data
        self.request.method = 'PUT'
        res = Profile().as_view()(self.request)
        if res.status_code == 200:
            messages.success(self.request, 'Username updated successfully!')
            return super(UsernameUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'An error occurred')
            return super(UsernameUpdateView, self).get(self.request, *self.args, **self.kwargs)


class PasswordUpdateView(LoginRequiredFormView):
    template_name = 'edit_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super(PasswordUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.request.data = form.cleaned_data
        self.request.method = 'PUT'
        res = PasswordUpdate().as_view()(self.request)
        if res.status_code == 200:
            messages.success(self.request, 'Password updated successfully!')
            return super(PasswordUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'An error occurred')
            return super(PasswordUpdateView, self).get(self.request, *self.args, **self.kwargs)


class DeleteAccountView(LoginRequiredFormView):
    template_name = 'delete_account.html'
    form_class = DeleteUserForm
    success_url = reverse_lazy('login')

    def get_initial(self):
        initial = super(DeleteAccountView, self).get_initial()
        initial.update({'username': self.request.user.username})
        return initial

    def get_form_kwargs(self):
        kwargs = super(DeleteAccountView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.request.method = 'DELETE'
        res = Profile().as_view()(self.request)
        if res.status_code == 204:
            messages.success(self.request, 'Account removed successfully!')
            return super(DeleteAccountView, self).form_valid(form)
        else:
            messages.error(self.request, 'An error occurred')
            return super(DeleteAccountView, self).get(self.request, *self.args, **self.kwargs)
