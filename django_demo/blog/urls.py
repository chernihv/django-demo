from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^post/$', views.post_create, name='create'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post_detail, name='detail'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user_detail, name='user'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^registration/$', views.user_registration, name='registration'),
    url(r'^user/reset/$', views.change_password_user, name='change_password'),
    url(r'^user/$', views.user_profile, name='profile'),
]
