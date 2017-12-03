from django.contrib import auth, messages
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404

from .. import constants, models, helpers, decorators, forms, services
from ..helpers import is_post, get_fields_request, go_home


@decorators.guest_only
def user_login(request):
    if is_post(request):
        username, password = get_fields_request(request, 'username', 'password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return go_home()
    form = forms.UserLoginForm()
    return render(request, 'blog/user_login.html', {'form': form})


@decorators.auth_only
def user_logout(request):
    auth.logout(request)
    return go_home()


@decorators.guest_only
def user_registration(request):
    if is_post(request):
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            username, password, email = get_fields_request(request, 'username', 'password', 'email')
            user = User.objects.create_user(username=username, password=password, email=email)
            user.groups.add(Group.objects.get(name=constants.Group.REGULAR_USER))
            auth.login(request, user)
            return go_home()
        else:
            messages.add_message(request, messages.INFO, 'User: ' + request.POST['username'] + ' already exist')
    else:
        form = forms.UserRegistrationForm()
    return render(request, 'blog/user_registration.html', {'form': form})


@decorators.auth_only
def user_profile(request):
    return render(request, 'blog/user_profile.html')


@decorators.auth_only
def change_password_user(request):
    messages.add_message(request, messages.INFO, 'You can not change the password')
    return render(request, 'blog/reset_password.html')


def user_detail(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'blog/user_detail.html', {'user': user})
