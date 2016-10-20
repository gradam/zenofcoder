from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics

from .models import Article, Tag
from .serializers import ArticleDetailSerializer
from .serializers import ArticlesListSerializer


class MultipleFieldLookupMixin:
    def get_object(self):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        filter = {}
        for field in self.lookup_fields:
            try:
                filter[field] = self.kwargs[field]
            except KeyError:
                pass
        return get_object_or_404(qs, **filter)


class ArticleDetail(MultipleFieldLookupMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):

    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    lookup_fields = ('id', 'slug')

    def get(self, request, **kwargs) -> Response:
        return self.retrieve(request, **kwargs)

    def post(self, request, **kwargs) -> Response:
        if kwargs.get('id') or kwargs.get('slug'):
            return self.partial_update(request, partial=True)
        else:
            return self.create(request)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class ArticlesByTags(APIView):
    def get(self, request, tags: str) -> Response:
        tags = set(tags.split('/'))
        qs = Article.objects.all()
        result = []
        for article in list(qs):
            if tags.issubset({str(tag) for tag in article.tags.all()}):
                result.append(article)
        serializer = ArticlesListSerializer(result, many=True)
        return Response(serializer.data)


class ArticlesList(APIView):
    def get(self, request) -> Response:
        qs = Article.objects.all()
        serializer = ArticlesListSerializer(qs, many=True)
        return Response(serializer.data)
