from noxcrux_server.mixins.Authenticated import LoginRequiredListView, LoginRequiredView, LoginRequiredFormView
from noxcrux_api.views.Friend import FriendList, FriendRequest
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
            'friends': FriendList().get(request).data,
            'requests': FriendRequest().get(request).data
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
        res = FriendList().post(self.request)
        if res.status_code == 201:
            messages.success(self.request, 'Friend request sent successfully!')
            return super(FriendAdd, self).form_valid(form)
        else:
            messages.error(self.request, 'An error occurred')
            return super(FriendAdd, self).get(self.request, *self.args, **self.kwargs)


class FriendDelete(LoginRequiredView):

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        res = FriendList().delete(request, username)
        if res.status_code == 204:
            messages.success(request, '%s removed successfully!' % username)
        else:
            messages.error(request, 'An error occurred')
        return HttpResponseRedirect(reverse('friend_list'))


class FriendRequestAccept(LoginRequiredView):

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        request.data = {'validated': True}
        res = FriendRequest().put(request, username)
        if res.status_code == 200:
            messages.success(request, '%s added successfully!' % username)
        else:
            messages.error(request, 'An error occurred')
        return HttpResponseRedirect(reverse('friend_list'))


class FriendRequestDelete(LoginRequiredView):

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        res = FriendRequest().delete(request, username)
        if res.status_code == 204:
            messages.success(request, '%s denied successfully!' % username)
        else:
            messages.error(request, 'An error occurred')
        return HttpResponseRedirect(reverse('friend_list'))
