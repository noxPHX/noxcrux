from rest_framework.permissions import BasePermission


class UsersPermissions(BasePermission):
    """
    Permission class for /users/ endpoint
    Only admins can access the list but anyone can create a new account
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        elif request.user and request.user.is_staff:
            return True
        return False


class UserUpdatePermissions(BasePermission):
    """
    Permission class for /user/username/ endpoint
    Only the self user and admins can get an user details and update them
    """
    def has_permission(self, request, view):
        if request.user.username == view.kwargs['username'] or request.user.is_staff:
            return True
        return False
