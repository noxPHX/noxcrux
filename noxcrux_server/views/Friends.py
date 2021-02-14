from noxcrux_server.mixins.Authenticated import LoginRequiredListView, LoginRequiredView
from noxcrux_api.views.Friend import FriendList, FriendRequest
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render


class FriendsView(LoginRequiredListView):
    template_name = 'friends.html'
    context_object_name = 'friends'

    def get(self, request, *args, **kwargs):
        context = {
            'friends': FriendList().get(request).data,
            'requests': FriendRequest().get(request).data
        }
        return render(request, self.template_name, context)


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
