from django.conf.urls import url

from .views import site_views, user_views, post_views

app_name = 'blog'
urlpatterns = [
    url(r'^$', site_views.index, name='index'),
    url(r'^contact/$', site_views.contact, name='contact'),
    url(r'^contact/question/$', site_views.new_questions, name='new_question'),
    url(r'^contact/question/(?P<question_id>[0-9]+)/hide/$', site_views.hide_question, name='hide_question'),

    url(r'^post/$', post_views.post_create, name='create'),
    url(r'^post/(?P<post_id>[0-9]+)/$', post_views.post_detail, name='detail'),
    url(r'^post/(?P<post_id>[0-9]+)/edit/$', post_views.post_edit, name='edit'),
    url(r'^post/(?P<post_id>[0-9]+)/delete/$', post_views.post_delete, name='delete'),
    url(r'^post/(?P<post_id>[0-9]+)/removeheaderimage/$', post_views.post_remove_header_image, name='remove_header'),
    url(r'^post/(?P<post_id>[0-9]+)/comment/$', post_views.post_comment, name='post_comment'),
    url(r'^post/comment/(?P<comment_id>[0-9]+)/hide/$', post_views.post_comment_hide, name='post_comment_hide'),

    url(r'^post/(?P<post_id>[0-9]+)/publish/$', post_views.publish_post, name='post_publish'),

    url(r'^post/(?P<post_id>[0-9]+)/block/$', post_views.block_create, name='block_create'),
    url(r'^post/(?P<post_id>[0-9]+)/block/save/$', post_views.block_save, name='block_save'),
    url(r'^post/(?P<post_id>[0-9]+)/block/delete/$', post_views.block_delete, name='block_delete'),

    url(r'^user/(?P<user_id>[0-9]+)/$', user_views.user_detail, name='user'),
    url(r'^login/$', user_views.user_login, name='login'),
    url(r'^logout/$', user_views.user_logout, name='logout'),
    url(r'^registration/$', user_views.user_registration, name='registration'),
    url(r'^user/reset/$', user_views.change_password_user, name='change_password'),
    url(r'^user/$', user_views.user_profile, name='profile'),
]
