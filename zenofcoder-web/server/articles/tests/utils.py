import pytest
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
    def create_article(author, title='Test article', content=ARTICLE_TEXT,
                       tags=None, **kwargs) -> Article:
        if tags is None:
            tags = []

        return Article.objects.create(title=title, content=content, author=author,
                                      tags=tags, **kwargs)
