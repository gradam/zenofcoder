# encoding: utf-8
from django.conf.urls import url
from .views import ArticleDetail, ArticlesList, ArticlesByTags


urlpatterns = [
    url(r'^all/$', ArticlesList.as_view(), name='all'),
    url(r'^id/(?P<id>\d+)/$', ArticleDetail.as_view(), name='id'),
    url(r'^tags/(?P<tags>[\w+/]+)', ArticlesByTags.as_view(), name='tags'),
]

