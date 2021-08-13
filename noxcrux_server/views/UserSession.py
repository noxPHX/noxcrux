from noxcrux_server.mixins.Authenticated import LoginRequiredListView, LoginRequiredView
from noxcrux_api.views.UserSession import UserSessionList, UserSessionRevoke
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


class UserSessions(LoginRequiredListView):
    template_name = 'sessions.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        return UserSessionList().as_view()(self.request).data


class DeleteUserSession(LoginRequiredView):

    def get(self, request, *args, **kwargs):
        session = kwargs['session']
        request.method = 'DELETE'
        res = UserSessionRevoke().as_view()(request, session=session)
        if res.status_code == 204:
            messages.success(request, 'Session revoked successfully!')
        else:
            messages.error(request, 'An error occurred')
        return HttpResponseRedirect(reverse('sessions'))
