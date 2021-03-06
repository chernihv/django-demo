from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import reverse
from django.conf import settings
from django.utils.crypto import get_random_string
from os import remove
import time


class Response:
    @staticmethod
    def go_home():
        return HttpResponseRedirect(reverse('blog:index'))

    @staticmethod
    def go_login():
        return HttpResponseRedirect(reverse('blog:login'))

    @staticmethod
    def redirect(url_name: str, *args, **kwargs):
        return HttpResponseRedirect(reverse(url_name, *args, **kwargs))


class File:
    @staticmethod
    def save(file, file_name: str):
        with open(settings.USER_FILES_PATH + file_name, 'wb+') as path:
            for chunk in file.chunks():
                path.write(chunk)

    @staticmethod
    def delete(file_name: str):
        remove(settings.USER_FILES_PATH + file_name)

    @staticmethod
    def get_valid_name(file):
        return get_random_string(25) + str((time.time())).replace('.', '') + file.name


class Request:
    @staticmethod
    def get_fields_request(request, *args):
        result = []
        for field in args:
            result.append(request.POST[field])
        return result

    @staticmethod
    def get_list_fields_request(request, *args):
        result = []
        for fields in args:
            result.append(request.POST.getlist(key=fields))
        return result

    @staticmethod
    def is_post(request: HttpRequest):
        return 'POST' in request.method

    @staticmethod
    def get_client_ip(request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class colorprint:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDSTR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, string: str, color=None):
        self._str = string
        self._color = color
        print("{begin}{string}{end}".format(begin=self._color, string=self._str, end=self.ENDSTR))
