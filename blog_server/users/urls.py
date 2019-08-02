from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.users, name='users'),
    url(r'^/(?P<username>[\w]+)$', views.users, name='user'),
    url(r'^/(?P<username>[\w]+)/avatar$', views.user_avatar, name='user_avatar'),
]