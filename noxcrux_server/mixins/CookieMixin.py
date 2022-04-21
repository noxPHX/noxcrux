from django.conf import settings


class CookieMixin(object):

    def __init__(self, *args, **kwargs):
        super(CookieMixin, self).__init__(*args, **kwargs)
        self._cookies = []

    def get_cookies(self):
        """
        Return an iterable of (args, kwargs) to be passed to set_cookie.
        """
        return self._cookies

    def add_cookie(self, *args, **kwargs):
        """
        Al given arguments will be passed to response.set_cookie later on.
        """
        self._cookies.append((args, kwargs))

    def dispatch(self, request, *args, **kwargs):
        """
        Get the response object from the parent class and sets the cookies on
        it accordingly.
        """
        response = super(CookieMixin, self).dispatch(request, *args, **kwargs)
        for cookie_args, cookie_kwargs in self.get_cookies():
            response.set_cookie(*cookie_args, **cookie_kwargs, httponly=True, samesite="Lax", secure=settings.SESSION_COOKIE_SECURE)
        return response
