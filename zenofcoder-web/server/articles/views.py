from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
    def get(self, request, **kwargs) -> Response:
        qs = get_object_or_404(Article, **kwargs)
        serializer = ArticleDetailSerializer(qs)
        return Response(serializer.data)

    def post(self, request, **kwargs) -> Response:
        instance = get_object_or_404(Article, **kwargs)
        serializer = ArticleDetailSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request) -> Response:
        article = Article()
        serializer = ArticleDetailSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticlesList(APIView):
    def get(self, request) -> Response:
        qs = get_list_or_404(Article)
        serializer = ArticlesListSerializer(qs, many=True)
        return Response(serializer.data)

