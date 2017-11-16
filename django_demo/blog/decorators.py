from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import reverse
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
