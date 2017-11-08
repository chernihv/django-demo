from django.shortcuts import render
from django.http import HttpRequest


# Create your views here.
def index(request: HttpRequest):
    return render(request, 'blog/index.html')


def contact(request: HttpRequest):
    return render(request, 'blog/contact.html')
