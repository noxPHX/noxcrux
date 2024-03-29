from noxcrux_server.mixins.Authenticated import LoginRequiredListView, LoginRequiredView, LoginRequiredFormView
from noxcrux_api.views.Friend import FriendList, FriendDestroy, FriendRequestsList, FriendRequestUpdate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from noxcrux_server.forms.User import FriendForm


class FriendsView(LoginRequiredListView):
    template_name = 'friends.html'
    context_object_name = 'friends'

    def get(self, request, *args, **kwargs):
        context = {
            'friends': FriendList().as_view()(request).data,
            'requests': FriendRequestsList().as_view()(request).data
        }
        return render(request, self.template_name, context)


class FriendAdd(LoginRequiredFormView):
    template_name = 'friend_add.html'
    form_class = FriendForm
    success_url = reverse_lazy('friend_list')

    def get_form_kwargs(self):
        kwargs = super(FriendAdd, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        self.request.data = form.cleaned_data
        res = FriendList().as_view()(self.request)
        if res.status_code == 201:
            messages.success(self.request, 'Friend request sent successfully!')
            return super(FriendAdd, self).form_valid(form)
        else:
            messages.error(self.request, 'An error occurred')
            return super(FriendAdd, self).get(self.request, *self.args, **self.kwargs)


class FriendDelete(LoginRequiredView):

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        request.method = 'DELETE'
        res = FriendDestroy().as_view()(request, username=username)
        if res.status_code == 204:
            messages.success(request, f'{username} removed successfully!')
        else:
            messages.error(request, 'An error occurred')
        return HttpResponseRedirect(reverse('friend_list'))


class FriendRequestAccept(LoginRequiredView):

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        request.method = 'PUT'
        res = FriendRequestUpdate().as_view()(request, username=username)
        if res.status_code == 200:
            messages.success(request, f'{username} added successfully!')
        else:
            messages.error(request, 'An error occurred')
        return HttpResponseRedirect(reverse('friend_list'))


class FriendRequestDelete(LoginRequiredView):

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        request.method = 'DELETE'
        res = FriendRequestUpdate().as_view()(request, username=username)
        if res.status_code == 204:
            messages.success(request, f'{username} denied successfully!')
        else:
            messages.error(request, 'An error occurred')
        return HttpResponseRedirect(reverse('friend_list'))
