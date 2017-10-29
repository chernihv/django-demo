from django.conf.urls import url
from .views.posts import post_list
from .views.questions import detail, result, vote, all_question

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^question/$', all_question),
    url(r'^question/(?P<question_id>[0-9]+)/$', detail),
    url(r'^question/(?P<question_id>[0-9]+)/results/$', result),
    url(r'^question/(?P<question_id>[0-9]+)/vote/(?P<choice_id>[0-9])+/$', vote),
]
