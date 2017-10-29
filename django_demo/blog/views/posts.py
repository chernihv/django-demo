from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.shortcuts import render
from ..models.posts import Post


def post_list(request: HttpRequest):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/posts/all_posts.html', {'posts': posts})
