from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import decorators


class Index(TemplateView):
    @staticmethod
    def get(request: HttpRequest, *args, **kwargs):
        return render(request, 'vue_js/base.html', {})

    @staticmethod
    def post(request: HttpRequest, *args, **kwargs):
        json_data = {'kolbaska': '1 kilogramchik'}
        return JsonResponse(json_data)
