from rest_framework import serializers

from .models import Article


class ArticleDetailSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    publication_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Article
        fields = ('title', 'author', 'content', 'tags', 'timestamp', 'publication_date', 'slug')


class ArticlesListSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    publication_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Article
        fields = ('title', 'author', 'tags', 'publication_date', 'timestamp', 'slug')

