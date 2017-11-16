from django.shortcuts import render, reverse, get_object_or_404, get_list_or_404
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import auth

from . import models
from . import forms
from . import helpers
from . import decorators


# Create your views here.
def index(request: HttpRequest):
    posts = models.Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})


@decorators.guest_only
def user_login(request: HttpRequest):
    if 'POST' in request.method:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return helpers.go_home()
    form = forms.UserLoginForm()
    return render(request, 'blog/user_login.html', {'form': form})


@decorators.my_login_require
def user_logout(request: HttpRequest):
    auth.logout(request)
    return helpers.go_home()


@decorators.guest_only
def user_registration(request: HttpRequest):
    message = None
    if 'POST' in request.method:
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            auth.login(request, user)
            return helpers.go_home()
        else:
            message = 'User: ' + request.POST['username'] + ' already exist'
    else:
        form = forms.UserRegistrationForm()
    return render(request, 'blog/user_registration.html', {'form': form, 'message': message})


@decorators.my_login_require
def user_profile(request: HttpRequest):
    return render(request, 'blog/user_profile.html')


@decorators.my_login_require
def change_password_user(request: HttpRequest):
    return helpers.go_home()


def contact(request: HttpRequest):
    message = None
    if 'POST' in request.method:
        form = forms.FeedbackForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.user_ip = helpers.get_client_ip(request)
            model.created_at = timezone.now()
            model.save()
            message = 'Question sent to admin'
    else:
        form = forms.FeedbackForm()
    return render(request, 'blog/contact.html', {'form': form, 'message': message})


@decorators.my_login_require
def post_create(request: HttpRequest):
    form = 1
    return render(request, 'blog/post_create.html', {'form': form})


def post_detail(request: HttpRequest, post_id: int):
    post = get_object_or_404(models.Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


def user_detail(request: HttpRequest, user_id: int):
    user = User.objects.get(pk=user_id)
    return render(request, 'blog/user_detail.html', {'user': user})
