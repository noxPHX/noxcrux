from noxcrux_server.mixins.Authenticated import LoginRequiredListView, LoginRequiredView
from noxcrux_api.views.Friend import FriendList
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


class FriendsView(LoginRequiredListView):
    template_name = 'friends.html'
    context_object_name = 'friends'

    def get_queryset(self):
        return FriendList().get(self.request).data


class FriendDelete(LoginRequiredView):

    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        res = FriendList().delete(request, username)
        if res.status_code == 204:
            messages.success(request, '%s removed successfully!' % username)
        else:
            messages.error(request, 'An error occurred')
        return HttpResponseRedirect(reverse('friend_list'))
