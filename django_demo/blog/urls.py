from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact/question/$', views.new_questions, name='new_question'),
    url(r'^contact/question/(?P<question_id>[0-9]+)/hide/$', views.hide_question, name='hide_question'),

    url(r'^post/$', views.post_create, name='create'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post_detail, name='detail'),
    url(r'^post/(?P<post_id>[0-9]+)/edit/$', views.post_edit, name='edit'),
    url(r'^post/(?P<post_id>[0-9]+)/delete/$', views.post_delete, name='delete'),
    url(r'^post/(?P<post_id>[0-9]+)/removeheaderimage/$', views.post_remove_header_image, name='remove_header_image'),
    url(r'^post/(?P<post_id>[0-9]+)/comment/$', views.post_comment, name='post_comment'),
    url(r'^post/comment/(?P<comment_id>[0-9]+)/hide/$', views.post_comment_hide, name='post_comment_hide'),

    url(r'^user/(?P<user_id>[0-9]+)/$', views.user_detail, name='user'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^registration/$', views.user_registration, name='registration'),
    url(r'^user/reset/$', views.change_password_user, name='change_password'),
    url(r'^user/$', views.user_profile, name='profile'),
]
