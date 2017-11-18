from django.shortcuts import render, reverse, get_object_or_404, get_list_or_404
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import auth, messages
from django.utils.crypto import get_random_string

from . import models
from . import forms
from . import helpers
from . import decorators


# Create your views here.
def index(request: HttpRequest):
    posts = models.Post.get_all_active_posts()
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


@decorators.auth_only
def user_logout(request: HttpRequest):
    auth.logout(request)
    return helpers.go_home()


@decorators.guest_only
def user_registration(request: HttpRequest):
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
            messages.add_message(request, messages.INFO, 'User: ' + request.POST['username'] + ' already exist')
    else:
        form = forms.UserRegistrationForm()
    return render(request, 'blog/user_registration.html', {'form': form})


@decorators.auth_only
def user_profile(request: HttpRequest):
    return render(request, 'blog/user_profile.html')


@decorators.auth_only
def change_password_user(request: HttpRequest):
    return helpers.go_home()


def contact(request: HttpRequest):
    if 'POST' in request.method:
        form = forms.FeedbackForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.user_ip = helpers.get_client_ip(request)
            model.created_at = timezone.now()
            model.save()
            messages.add_message(request, messages.INFO, 'Question sent to admin')
    else:
        form = forms.FeedbackForm()
    return render(request, 'blog/contact.html', {'form': form})


@decorators.admin_only
def new_questions(request: HttpRequest):
    questions = models.Feedback.objects.filter(is_read=False)
    return render(request, 'blog/questions.html', {'questions': questions})


@decorators.admin_only
def hide_question(request: HttpRequest, question_id: int):
    question = models.Feedback.objects.get(pk=question_id)
    question.is_read = True
    question.save()
    return HttpResponseRedirect(reverse('blog:new_question'))


@decorators.auth_only
def post_create(request: HttpRequest):
    if 'POST' in request.method:
        form = forms.PostForm(request.POST)
        image_form = forms.PostFileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.user = request.user
            post.save()
            if image_form.is_valid():
                file = request.FILES['file']
                saved_name = get_random_string() + file.name
                helpers.save_file(file, saved_name)
                file_model = models.PostFile(post_id=post.id, file_type=models.PostFile.POST_IMAGE,
                                             file_name=saved_name, created_at=timezone.now())
                file_model.save()
            return HttpResponseRedirect(reverse('blog:detail', args=[post.id]))
    else:
        form = forms.PostForm()
        image_form = forms.PostFileForm()
    return render(request, 'blog/post_create.html', {'form': form, 'image_form': image_form})


@decorators.auth_only
def post_edit(request: HttpRequest, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    form = forms.PostForm(instance=post)
    image_form = forms.PostFileForm()
    if request.user.id == post.user_id:
        if 'POST' in request.method:
            form = forms.PostForm(request.POST, instance=post)
            image_form = forms.PostFileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                if image_form.is_valid():
                    old_post = post.postfile_set.filter(file_type=models.PostFile.POST_IMAGE, is_removed=False).first()
                    old_post.is_removed = True
                    old_post.save()
                    file = request.FILES['file']
                    saved_name = get_random_string() + file.name
                    helpers.save_file(file, saved_name)
                    file_model = models.PostFile(post_id=post.id, file_type=models.PostFile.POST_IMAGE,
                                                 file_name=saved_name, created_at=timezone.now())
                    file_model.save()
            return HttpResponseRedirect(reverse('blog:detail', args=[post.id]))
        else:
            return render(request, 'blog/post_edit.html', {'form': form, 'image_form': image_form})
    else:
        return HttpResponseForbidden()


@decorators.auth_only
def post_delete(request: HttpRequest, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    if request.user.id == post.user_id:
        post.is_removed = True
        post.save()
        return helpers.go_home()
    else:
        return HttpResponseForbidden()


def post_detail(request: HttpRequest, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


def user_detail(request: HttpRequest, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'blog/user_detail.html', {'user': user})
