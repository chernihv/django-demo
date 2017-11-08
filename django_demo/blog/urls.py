from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post_detail, name='detail'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user_detail, name='user'),
]
