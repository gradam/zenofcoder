from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Article
from .serializers import ArticleDetailSerializer, ArticlesListSerializer


class ArticlesByTags(APIView):
    def get(self, request, tags: str) -> Response:
        tags = tags.split('/')
        qs = get_list_or_404(Article, tags__contains=tags)
        serializer = ArticlesListSerializer(qs, many=True)
        return Response(serializer.data)


class ArticleDetail(APIView):
    def get(self, request, id: str) -> Response:
        qs = get_object_or_404(Article, pk=id)
        serializer = ArticleDetailSerializer(qs)
        return Response(serializer.data)


class ArticlesList(APIView):
    def get(self, request) -> Response:
        qs = get_list_or_404(Article)
        serializer = ArticlesListSerializer(qs, many=True)
        return Response(serializer.data)

