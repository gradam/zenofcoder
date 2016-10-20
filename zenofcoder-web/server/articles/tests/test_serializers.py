from .utils import BaseTestClass, User
from articles.serializers import ArticleDetailSerializer, ArticlesListSerializer
from articles.models import Article


class TestArticleSerializer(BaseTestClass):
    def test_article_detail_serializer(self, base_article: Article):
        serializer = ArticleDetailSerializer(base_article)
        data = {
            'title': base_article.title,
            'author': base_article.author.id,
            'content': base_article.content,
            'tags': [str(x) for x in base_article.tags.all()],
            'timestamp': base_article.timestamp.strftime('%Y-%m-%d %H:%M'),
            'publication_date': base_article.publication_date.strftime('%Y-%m-%d %H:%M'),
            'slug': base_article.slug,
            'pk': base_article.pk
        }

        assert serializer.data == data

    def test_create_in_detail_serializer(self, admin_user: User):
        title = 'test title1'
        author = admin_user
        content = 'test content'
        tags = ['tag1', 'tag2']

        data = {
            'title': title,
            'author': author.pk,
            'content': content,
            'tags': tags
        }
        serializer = ArticleDetailSerializer(data=data)
        assert serializer.is_valid()
        serializer.save()
        assert Article.objects.get(title=title, content=content)

    def test_article_list_serializer(self, base_article: Article):
        serializer = ArticlesListSerializer(base_article)
        data = {
            'title': base_article.title,
            'author': base_article.author.id,
            'tags': [str(x) for x in base_article.tags.all()],
            'timestamp': base_article.timestamp.strftime('%Y-%m-%d %H:%M'),
            'publication_date': base_article.publication_date.strftime('%Y-%m-%d %H:%M'),
            'slug': base_article.slug
        }

        assert serializer.data == data
