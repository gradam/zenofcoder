# encoding: utf-8
from django.utils import timezone
from django.contrib.auth import get_user_model
from articles.models import Article, create_slug
from .utils import BaseTestClass


User = get_user_model()


class TestArticleModel(BaseTestClass):

    def test_article_to_user(self, admin_user: User):
        article1 = self.create_article(author=admin_user)
        article2 = self.create_article(author=admin_user,  title='test 2')
        assert [article2, article1] == list(Article.objects.filter(author=admin_user))

    def test_get_by_tag(self, base_article: Article):
        assert [base_article] == list(Article.objects.filter(tags__tag='test'))

    def test_add_tags(self, base_article: Article):
        base_article.add_tags(['user', 'user2'])
        base_article.save()
        assert [base_article] == list(Article.objects.filter(tags__tag='user'))

    def test_remove_tags(self, base_article: Article):
        base_article.remove_tags(['test', 'article'])
        base_article.save()
        assert [base_article] == list(Article.objects.filter(tags__tag='admin'))

    def test_published(self, base_article: Article):
        assert base_article.published

    def test_not_published_yet(self, base_article: Article):
        base_article.publication_date += timezone.timedelta(hours=1)
        base_article.save()
        assert not base_article.published

    def test_str_representation(self, base_article: Article):
        assert str(base_article) == base_article.title

    def test_create_slug(self, base_article: Article):
        create_slug(base_article)
        assert base_article.slug == 'test-article'

    def test_multiple_slug(self, admin_user: User):
        article1 = self.create_article(author=admin_user)
        article2 = self.create_article(author=admin_user)
        articles_number = len(Article.objects.filter(title=article1.title))
        assert article1.slug == 'test-article'
        assert article2.slug == 'test-article-{}'.format(articles_number)

    def test_multiple_slug_2(self, admin_user: User):
        article1 = self.create_article(author=admin_user)
        article2 = self.create_article(author=admin_user, title='Different title')
        article3 = self.create_article(author=admin_user)
        articles_number = len(Article.objects.filter(title=article1.title))
        assert article3.slug == 'test-article-{}'.format(articles_number)
