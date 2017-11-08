from django.shortcuts import render
from django.http import HttpRequest
from . import models as blog_models


# Create your views here.
def index(request: HttpRequest):
    return render(request, 'blog/index.html')


def contact(request: HttpRequest):
    feedback_model = blog_models.Feedback()
    return render(request, 'blog/contact.html', {'feedback_model': feedback_model})
