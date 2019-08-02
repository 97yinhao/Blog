from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/(?P<author_id>[\w]+)$', views.topics, name='topics'),
    url(r'^/(?P<author_id>[\w]+)/topics$', views.topics)
]