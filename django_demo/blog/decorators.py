from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, Group
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


def superuser_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        else:
            return helpers.go_login()

    return wrapper


def permission_require(permission):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.has_perm(permission):
                return func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()

        return wrapper

    return decorator


def group_require(name):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                group = Group.objects.get(name=name)
                if group in request.user.groups.all() or request.user.is_superuser:
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden()
            else:
                return helpers.go_login()

        return wrapper

    return decorator
