# encoding: utf-8
from django.contrib.auth.models import User

import pytest

from articles.models import Article

ARTICLE_TEXT = """
If you don’t specify primary_key=True for any fields in your model, Django will automatically
 add an IntegerField to hold the primary key, so you don’t need to set primary_
 key=True on any of your fields unless you want to override the default primary-key behavior.
 For more, see Automatic primary key fields.
"""


@pytest.mark.django_db
class TestArticleModel:
    @pytest.fixture
    def admin_user(self):
        return User.objects.create_superuser('admin', 'admi.admin@admin.com', 'admin')

    @staticmethod
    def create_article(author, title='Test_article', text=ARTICLE_TEXT,
                       short='If you don\'t specify', tags=None, **kwargs):
        if tags is None:
            tags = []

        return Article.objects.create(title=title, text=text, short=short, author=author,
                                      tags=tags, **kwargs)

    def test_article_creation(self, admin_user):
        self.create_article(author=admin_user)

    def test_article_to_user(self, admin_user):
        article1 = self.create_article(author=admin_user)
        article2 = self.create_article(author=admin_user,  title='test 2')
        assert [article1, article2] == list(Article.objects.filter(author=admin_user))

    def test_tags(self, admin_user):
        article = self.create_article(author=admin_user)
        article.tags = ['test', 'article', 'admin']
        assert {'test', 'article', 'admin'} == set(article.tags)

    def test_get_by_tag(self, admin_user):
        article = self.create_article(author=admin_user, tags=['test', 'article', 'admin'])
        assert [article] == list(Article.objects.filter(tags__contains=['test']))
