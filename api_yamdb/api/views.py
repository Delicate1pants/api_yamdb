from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitlesReadSerializer, TitlesWriteSerializer)
from reviews.models import Category, Comment, Genre, Review, Titles


class CustomModelViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    lookup_field = "slug"
    serializer_class = CategorySerializer
    # permission_classes = []
    filter_backends = [SearchFilter]
    search_fields = ("name",)


class GenreViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    # permission_classes = []
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    # permission_classes = []

    def get_serializer_class(self):
        if self.request.method in ['list', 'retrieve']:
            return TitlesReadSerializer
        return TitlesWriteSerializer


class ReviewViewSet(CustomModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (AuthorOrReadOnly)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        get_object_or_404(Titles, pk=title_id)
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset


class CommentViewSet(CustomModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (AuthorOrReadOnly)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        get_object_or_404(Review, pk=review_id)
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset
