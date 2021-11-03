from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Comment, Review, Title


class CustomModelViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(CustomModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly)
    pagination_class = PageNumberPagination
    pagination_class.page_size = 3

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        get_object_or_404(Title, pk=title_id)
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset


class CommentViewSet(CustomModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly)
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        get_object_or_404(Review, pk=review_id)
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset
