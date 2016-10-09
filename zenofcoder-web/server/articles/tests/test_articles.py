# encoding: utf-8
import pytest
from django.utils import timezone
from django.contrib.auth import get_user_model
from articles.models import Article


User = get_user_model()


@pytest.mark.django_db
class BaseTestClass:
    ARTICLE_TEXT = """
    If you don’t specify primary_key=True for any fields in your model, Django will automatically
     add an IntegerField to hold the primary key, so you don’t need to set primary_
     key=True on any of your fields unless you want to override the default primary-key behavior.
     For more, see Automatic primary key fields.
    """

    @pytest.fixture
    def admin_user(self) -> User:
        return User.objects.create_superuser('admin', 'admi.admin@admin.com', 'admin')

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user('user', 'user.user@user.com', 'user')

    @pytest.fixture
    def base_article(self, admin_user) -> Article:
        return self.create_article(author=admin_user, tags=['test', 'article', 'admin'])

    @staticmethod
    def create_article(author, title='Test_article', content=ARTICLE_TEXT,
                       tags=None, **kwargs) -> Article:
        if tags is None:
            tags = []

        return Article.objects.create(title=title, content=content, author=author,
                                      tags=tags, **kwargs)


class TestArticleModel(BaseTestClass):

    def test_article_to_user(self, admin_user: User):
        article1 = self.create_article(author=admin_user)
        article2 = self.create_article(author=admin_user,  title='test 2')
        assert [article2, article1] == list(Article.objects.filter(author=admin_user))

    def test_tags(self, base_article: Article):
        base_article.tags = ['test', 'article', 'admin']
        assert {'test', 'article', 'admin'} == set(base_article.tags)

    def test_get_by_tag(self, base_article: Article):
        assert [base_article] == list(Article.objects.filter(tags__contains=['test']))

    def test_add_tags(self, base_article: Article):
        base_article.add_tags('user', 'user2')
        base_article.save()
        assert [base_article] == list(Article.objects.filter(tags__contains=['user']))

    def test_remove_tags(self, base_article: Article):
        base_article.remove_tags('test', 'article')
        base_article.save()
        assert [base_article] == list(Article.objects.filter(tags__contains=['admin']))

    def test_published(self, base_article: Article):
        assert base_article.published

    def test_not_published_yet(self, base_article: Article):
        base_article.publication_date += timezone.timedelta(hours=1)
        base_article.save()
        assert not base_article.published

    def test_str_representation(self, base_article: Article):
        assert str(base_article) == base_article.title
