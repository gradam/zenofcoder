# encoding: utf-8
from django.conf.urls import url
from .views import ArticleDetail, ArticlesList, ArticlesByTags


urlpatterns = [
    url(r'^$', ArticlesList.as_view(), name='all'),
    url(r'^id/(?P<id>\d+)/$', ArticleDetail.as_view(), name='id'),
    url(r'^slug/(?P<slug>[-\w]+)/$', ArticleDetail.as_view(), name='slug'),
    url(r'^tags/(?P<tags>[\w+/]+$)', ArticlesByTags.as_view(), name='tags'),
    url(r'^create/$', ArticleDetail.as_view(), name='create', )
]

