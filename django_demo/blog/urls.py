from django.conf.urls import url
from . import views

module_name = 'question'

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^question/$', views.all_question),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.detail),
    url(r'^question/(?P<question_id>[0-9]+)/results/$', views.result),
    url(r'^question/(?P<question_id>[0-9]+)/vote/$', views.vote),
]
