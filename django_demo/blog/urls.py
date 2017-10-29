from django.conf.urls import url
from .views.posts import post_list
from .views.questions import detail, result, vote, all_question

app_name = 'blog'
urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^question/$', all_question, name='question'),
    url(r'^question/(?P<question_id>[0-9]+)/$', detail, name='question_detail'),
    url(r'^question/(?P<question_id>[0-9]+)/results/$', result, name='vote_result'),
    url(r'^question/(?P<question_id>[0-9]+)/vote/(?P<choice_id>[0-9])+/$', vote, name='choice_vote'),
]
