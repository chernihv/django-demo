from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.http import HttpResponse, HttpRequest


def post_list(request: HttpRequest):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def all_question(request: HttpRequest):
    return HttpResponse('All questions')


def detail(request: HttpRequest, question_id: int):
    return HttpResponse('Question detail: {det}'.format(det=question_id))


def result(request: HttpRequest, question_id: int):
    return HttpResponse('Result questions: {q_id}'.format(q_id=question_id))


def vote(request: HttpRequest, question_id: int):
    return HttpResponse('Vote on question: {q_id}'.format(q_id=question_id))
