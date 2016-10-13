from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'author', 'content', 'tags', 'timestamp', 'publication_date', 'slug')
