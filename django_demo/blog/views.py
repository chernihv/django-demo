from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone

from . import models
from . import forms
from . import helpers


# Create your views here.
def index(request: HttpRequest):
    posts = models.Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})


def contact(request: HttpRequest):
    return render(request, 'blog/contact.html')


def post_detail(request: HttpRequest, post_id: int):
    post = get_object_or_404(models.Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


def user_detail(request: HttpRequest, user_id: int):
    user = User.objects.get(pk=user_id)
    return render(request, 'blog/user_detail.html', {'user': user})
