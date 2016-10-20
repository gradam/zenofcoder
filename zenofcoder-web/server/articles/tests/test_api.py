# encoding: utf-8
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.test import APIClient
from rest_framework import status

import pytest

from articles.models import Article, create_slug
from articles.serializers import ArticleDetailSerializer, ArticlesListSerializer
from .utils import BaseTestClass, User


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

    def test_create_article(self, admin_user: User):
        number_of_articles = Article.objects.all().count()
        data = {
            'title': 'Create test.',
            'author': admin_user.pk,
            'content': 'Some very interesting content',
            'tags': ['tag1', 'tag2'],
        }
        url = reverse('articles:create')
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Article.objects.all().count() == number_of_articles + 1

    def test_data_in_created_article(self, admin_user: User):
        data = {
            'title': 'Create test.',
            'author': admin_user.pk,
            'content': 'Some very interesting content',
            'tags': ['tag1', 'tag2'],
        }
        url = reverse('articles:create')
        response = self.client.post(url, data=data, format='json')
        pk = response.data['pk']
        new_article = Article.objects.get(pk=pk)
        assert response.data == ArticleDetailSerializer(new_article).data

    def test_delete_article_by_id(self, base_article: Article):
        url = reverse('articles:id', kwargs={'id': base_article.id})
        response = self.client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(ObjectDoesNotExist):
            Article.objects.get(id=base_article.id)

    def test_delete_article_by_slug(self, base_article: Article):
        url = reverse('articles:slug', kwargs={'slug': base_article.slug})
        response = self.client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(ObjectDoesNotExist):
            Article.objects.get(slug=base_article.slug)

    def test_get_by_slug(self, base_article: Article):
        url = reverse('articles:slug', kwargs={'slug': base_article.slug})
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == ArticleDetailSerializer(base_article).data

    def test_get_all_articles(self, admin_user: User):
        article1 = self.create_article(author=admin_user)
        article2 = self.create_article(author=admin_user)
        url = reverse('articles:all')
        response = self.client.get(url, format='json')
        serializer = ArticlesListSerializer([article2, article1], many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_get_one_by_tags(self, admin_user: User):
        article1 = self.create_article(author=admin_user, tags=['test1', 'test2', 'test3'])
        article2 = self.create_article(author=admin_user, tags=['test1', 'test4', 'test3'])
        url = reverse('articles:tags', kwargs={'tags': 'test2/test1'})
        response = self.client.get(url, format='json')
        serializer = ArticlesListSerializer([article1], many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_get_multiple_by_tags(self, admin_user: User):
        article1 = self.create_article(author=admin_user, tags=['test1', 'test2', 'test3'])
        article2 = self.create_article(author=admin_user, tags=['test1', 'test4', 'test3'])
        article3 = self.create_article(author=admin_user, tags=['test1', 'test4', 'test33'])
        url = reverse('articles:tags', kwargs={'tags': 'test1/test3'})
        response = self.client.get(url, format='json')
        serializer = ArticlesListSerializer([article2, article1], many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data
