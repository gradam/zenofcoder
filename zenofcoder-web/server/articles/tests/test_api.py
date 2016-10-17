# encoding: utf-8
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from articles.models import Article, create_slug
from articles.serializers import ArticleDetailSerializer, ArticlesListSerializer
from .utils import BaseTestClass


class TestArticleApiEndpoint(BaseTestClass):
    client = APIClient()

    def test_get_article_by_id(self, base_article: Article):
        url = reverse('articles:id', kwargs={'id': base_article.pk})
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == ArticleDetailSerializer(base_article).data

    def test_post_article_by_id(self, base_article: Article):
        url = reverse('articles:id', kwargs={'id': base_article.pk})
        new_title = 'New title'
        new_slug = create_slug(new_title)
        response = self.client.post(url, data={'title': new_title}, format='json')
        updated = Article.objects.get(pk=base_article.pk)
        assert response.status_code == status.HTTP_200_OK
        assert updated.title == new_title
        assert updated.slug == new_slug

    def test_post_article_not_valid_data(self, base_article: Article):
        url = reverse('articles:id', kwargs={'id': base_article.pk})
        response = self.client.post(url, data={'author': 'something'}, format='json')
        updated = Article.objects.get(pk=base_article.pk)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert updated == base_article

    def test_get_by_slug(self, base_article: Article):
        url = reverse('articles:slug', kwargs={'slug': base_article.slug})
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == ArticleDetailSerializer(base_article).data

    def test_get_all_articles(self, admin_user):
        article1 = self.create_article(author=admin_user)
        article2 = self.create_article(author=admin_user)
        url = reverse('articles:all')
        response = self.client.get(url, format='json')
        serializer = ArticlesListSerializer([article2, article1], many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_get_one_by_tags(self, admin_user):
        article1 = self.create_article(author=admin_user, tags=['test1', 'test2', 'test3'])
        article2 = self.create_article(author=admin_user, tags=['test1', 'test4', 'test3'])
        url = reverse('articles:tags', kwargs={'tags': 'test2/test1'})
        response = self.client.get(url, format='json')
        serializer = ArticlesListSerializer([article1], many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_get_multiple_by_tags(self, admin_user):
        article1 = self.create_article(author=admin_user, tags=['test1', 'test2', 'test3'])
        article2 = self.create_article(author=admin_user, tags=['test1', 'test4', 'test3'])
        url = reverse('articles:tags', kwargs={'tags': 'test1/test3'})
        response = self.client.get(url, format='json')
        serializer = ArticlesListSerializer([article2, article1], many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data
