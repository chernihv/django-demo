from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone

from .. import constants, models, helpers, decorators, forms, services
from ..helpers import get_client_ip, redirect, is_post


def index(request):
    posts = models.Post.get_all_active_posts()
    return render(request, 'blog/index.html', {'posts': posts})


def contact(request):
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
def new_questions(request):
    questions = models.Feedback.get_valid_questions()
    return render(request, 'blog/questions.html', {'questions': questions})


@decorators.superuser_only
def hide_question(request, question_id: int):
    models.Feedback.hide_question(question_id)
    return redirect('blog:new_question')
