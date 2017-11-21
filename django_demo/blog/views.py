from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from . import decorators
from . import forms
from . import models
from . import constants
from .helpers import (redirect, is_post, go_home, get_client_ip,
                      get_fields_request, save_file, get_valid_name)


def index(request: HttpRequest):
    posts = models.Post.get_all_active_posts()
    return render(request, 'blog/index.html', {'posts': posts})


@decorators.guest_only
def user_login(request: HttpRequest):
    if is_post(request):
        username, password = get_fields_request(request, 'username', 'password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return go_home()
    form = forms.UserLoginForm()
    return render(request, 'blog/user_login.html', {'form': form})


@decorators.auth_only
def user_logout(request: HttpRequest):
    auth.logout(request)
    return go_home()


@decorators.guest_only
def user_registration(request: HttpRequest):
    if is_post(request):
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            username, password, email = get_fields_request(request, 'username', 'password', 'email')
            user = User.objects.create_user(username=username, password=password, email=email)
            auth.login(request, user)
            return go_home()
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
    return go_home()


def contact(request: HttpRequest):
    if is_post(request):
        form = forms.FeedbackForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.user_ip = get_client_ip(request)
            model.created_at = timezone.now()
            model.save()
            messages.add_message(request, messages.INFO, 'Question sent to admin')
    else:
        form = forms.FeedbackForm()
    return render(request, 'blog/contact.html', {'form': form})


@decorators.superuser_only
def new_questions(request: HttpRequest):
    questions = models.Feedback.get_valid_questions()
    return render(request, 'blog/questions.html', {'questions': questions})


@decorators.superuser_only
def hide_question(request: HttpRequest, question_id: int):
    models.Feedback.hide_question(question_id)
    return redirect('blog:new_question')


# TODO Сделать загрузку нескольких изображений с возможностью встраивать их в текст.
@decorators.group_require(constants.Group.REGULAR_USER)
def post_create(request: HttpRequest):
    if is_post(request):
        form = forms.PostForm(request.POST)
        image_form = forms.PostFileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.user = request.user
            post.save()
            if image_form.is_valid():
                file = request.FILES['file']
                saved_name = get_valid_name(file)
                save_file(file, saved_name)
                models.PostFile(post_id=post.id, file_type=models.PostFile.POST_IMAGE,
                                file_name=saved_name, created_at=timezone.now()).save()
            return redirect('blog:detail', args=[post.id])
    else:
        form = forms.PostForm()
        image_form = forms.PostFileForm()
    return render(request, 'blog/post_create.html', {'form': form, 'image_form': image_form})


@decorators.group_require(constants.Group.REGULAR_USER)
def post_edit(request: HttpRequest, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    form = forms.PostForm(instance=post)
    image_form = forms.PostFileForm()
    if request.user.id == post.user_id:
        if is_post(request):
            form = forms.PostForm(request.POST, instance=post)
            image_form = forms.PostFileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                if image_form.is_valid():
                    post.disable_post_image()
                    file = request.FILES['file']
                    saved_name = get_valid_name(file)
                    save_file(file, saved_name)
                    models.PostFile(post_id=post.id, file_type=models.PostFile.POST_IMAGE,
                                    file_name=saved_name, created_at=timezone.now()).save()
            return redirect('blog:detail', args=[post.id])
        else:
            return render(request, 'blog/post_edit.html', {'form': form, 'image_form': image_form})
    else:
        return HttpResponseForbidden()


@decorators.group_require(constants.Group.REGULAR_USER)
def post_delete(request: HttpRequest, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    if request.user.id == post.user_id:
        post.remove_post()
        return go_home()
    else:
        return HttpResponseForbidden()


def post_detail(request: HttpRequest, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


@decorators.group_require(constants.Group.REGULAR_USER)
def post_remove_header_image(request: HttpRequest, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    post.disable_post_image()
    return redirect('blog:edit', args=[post_id])


@decorators.group_require(constants.Group.REGULAR_USER)
def post_comment(request: HttpRequest, post_id: int):
    if is_post(request):
        comment_text = request.POST['post_comment']
        models.PostComment(post_id=post_id, comment_text=comment_text, created_at=timezone.now(),
                           user_id=request.user.id).save()
        return redirect('blog:detail', args=[post_id])


@decorators.group_require(constants.Group.REGULAR_USER)
def post_comment_hide(request: HttpRequest, comment_id: int):
    comment = get_object_or_404(models.PostComment, pk=comment_id)
    comment.hide_comment()
    return redirect('blog:detail', args=[comment.post_id])


def user_detail(request: HttpRequest, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'blog/user_detail.html', {'user': user})
