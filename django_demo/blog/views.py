from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import reverse
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
    if 'POST' in request.method:
        form = forms.FeedbackForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.user_ip = helpers.get_client_ip(request)
            model.created_at = timezone.now()
            model.save()
            message = 'Question sent to admin'
            return render(request, 'blog/contact.html', {'form': form, 'message': message})
    else:
        form = forms.FeedbackForm()
    return render(request, 'blog/contact.html', {'form': form})


def post_detail(request: HttpRequest, post_id: int):
    post = get_object_or_404(models.Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


def user_detail(request: HttpRequest, user_id: int):
    user = User.objects.get(pk=user_id)
    return render(request, 'blog/user_detail.html', {'user': user})
