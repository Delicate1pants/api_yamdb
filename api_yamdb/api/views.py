from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from reviews.models import Titles, Category, Genre
from .serializers import (GenreSerializer, CategorySerializer, TitlesReadSerializer, TitlesWriteSerializer)

User = get_user_model()


class CategoryViewSet(mixins.ListModelMixin,
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    queryset = Category.objects.all()
    lookup_field = "slug"
    serializer_class = CategorySerializer
    #permission_classes = []
    filter_backends = [SearchFilter]
    search_fields = ("name",)


class GenreViewSet(mixins.ListModelMixin,
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    #permission_classes = []
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    #permission_classes = []
    def get_serializer_class(self):
        if self.request.method in ['list', 'retrieve']:
            return TitlesReadSerializer
        return TitlesWriteSerializer
