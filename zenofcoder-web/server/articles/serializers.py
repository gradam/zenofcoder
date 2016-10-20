from django.utils import timezone
from rest_framework import serializers

from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    def to_representation(self, instance: Tag) -> str:
        return instance.tag

    def to_internal_value(self, tag: str) -> dict:
        return {'tag': tag}

    class Meta:
        model = Tag
        fields = ('tag', )


class BaseArticleSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M', default=timezone.now)
    publication_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', default=timezone.now)
    tags = TagSerializer(many=True)
    slug = serializers.SlugField(default=None)


class ArticleDetailSerializer(BaseArticleSerializer):

    class Meta:
        model = Article
        fields = ('title', 'author', 'content', 'tags', 'timestamp', 'publication_date', 'slug',
                  'pk')

    def create(self, validated_data) -> Article:
        tags = validated_data.pop('tags')
        article = Article.objects.create(**validated_data)
        article.add_tags([tag['tag'] for tag in tags])
        return article

    def update(self, instance: Article, validated_data):
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.set_tags([tag['tag'] for tag in tags])
        return super().update(instance, validated_data)


class ArticlesListSerializer(BaseArticleSerializer):

    class Meta:
        model = Article
        fields = ('title', 'author', 'tags', 'publication_date', 'timestamp', 'slug')
