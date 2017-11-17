from django.http import HttpResponseForbidden
from . import helpers


def auth_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return helpers.go_login()

    return wrapper


def guest_only(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return helpers.go_home()

    return wrapper


def admin_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        else:
            return helpers.go_login()

    return wrapper
