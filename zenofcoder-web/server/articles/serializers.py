from django.utils import timezone
from rest_framework import serializers

from .models import Article


class ArticleDetailSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M', default=timezone.now)
    publication_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', default=timezone.now)
    slug = serializers.SlugField(default=None)

    class Meta:
        model = Article
        fields = ('title', 'author', 'content', 'tags', 'timestamp', 'publication_date', 'slug',
                  'pk')


class ArticlesListSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    publication_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Article
        fields = ('title', 'author', 'tags', 'publication_date', 'timestamp', 'slug')

