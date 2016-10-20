from .utils import BaseTestClass
from articles.serializers import ArticleDetailSerializer, ArticlesListSerializer
from articles.models import Article


class TestArticleSerializer(BaseTestClass):
    def test_article_detail_serializer(self, base_article: Article):
        serializer = ArticleDetailSerializer(base_article)
        data = {
            'title': base_article.title,
            'author': base_article.author.id,
            'content': base_article.content,
            'tags': base_article.tags,
            'timestamp': base_article.timestamp.strftime('%Y-%m-%d %H:%M'),
            'publication_date': base_article.publication_date.strftime('%Y-%m-%d %H:%M'),
            'slug': base_article.slug,
            'pk': base_article.pk
        }

        assert serializer.data == data

    def test_article_list_serializer(self, base_article: Article):
        serializer = ArticlesListSerializer(base_article)
        data = {
            'title': base_article.title,
            'author': base_article.author.id,
            'tags': base_article.tags,
            'timestamp': base_article.timestamp.strftime('%Y-%m-%d %H:%M'),
            'publication_date': base_article.publication_date.strftime('%Y-%m-%d %H:%M'),
            'slug': base_article.slug
        }

        assert serializer.data == data
