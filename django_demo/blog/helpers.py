from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import reverse
from django.conf import settings
from os import remove


def get_client_ip(request: HttpRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def go_home():
    return HttpResponseRedirect(reverse('blog:index'))


def go_login():
    return HttpResponseRedirect(reverse('blog:login'))


def save_file(file, file_name: str):
    path_to_save = settings.BASE_DIR + '/blog/static/blog/user_files/'
    with open(path_to_save + file_name, 'wb+') as path:
        for chunk in file.chunks():
            path.write(chunk)


def delete_file(file_name: str):
    path_to_del = settings.BASE_DIR + '/blog/static/blog/user_files/'
    remove(path_to_del + file_name)
