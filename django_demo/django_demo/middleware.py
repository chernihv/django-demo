from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import reverse, NoReverseMatch


class LoginRequiredMiddleware(MiddlewareMixin):
    @staticmethod
    def process_view(request: HttpRequest, view_func, *args, **kwargs):
        """
        If you need to give access to execute view, add this attribute to view
         _no_login_require equal True, or use decorator no_login_require
        """
        assert hasattr(settings, 'LOGIN_URL'), "Does not set parameter LOGIN_URL in settings"
        assert hasattr(request,
                       'user'), "Request does not have attribute user, perhaps, not enabled AuthenticationMiddleware"
        if not request.user.is_authenticated:
            if not (hasattr(view_func, '_no_login_require') and getattr(view_func, '_no_login_require')):
                try:
                    if request.get_full_path() != reverse(settings.LOGIN_URL):
                        return HttpResponseRedirect(reverse(settings.LOGIN_URL))
                except NoReverseMatch:
                    if request.get_full_path() != settings.LOGIN_URL:
                        return HttpResponseRedirect(settings.LOGIN_URL)
