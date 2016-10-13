# encoding: utf-8
from django.conf.urls import url
from .views import ArticlesView


urlpatterns = [
    url(r'^all/$', ArticlesView.as_view()),
]

