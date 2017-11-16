from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import reverse
from . import helpers


def my_login_require(func):
    def wrapper(request, *args):
        if request.user.is_authenticated:
            return func(request, *args)
        else:
            return HttpResponseRedirect(reverse('blog:login'))

    return wrapper


def guest_only(func):
    def wrapper(request, *args):
        if not request.user.is_authenticated:
            return func(request, *args)
        else:
            return helpers.go_home()

    return wrapper
