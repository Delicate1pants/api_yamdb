from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import six
from rest_framework import mixins, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAuthenticated
from .serializers import (AuthenticationSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitlesReadSerializer, TitlesWriteSerializer,
                          UserSerializer)
from reviews.models import Category, Comment, Genre, Review, Titles, User


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def get_access_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            resp = Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            resp = Response(request.data, status=status.HTTP_200_OK)
        print(user)
        confirmation_code = account_activation_token.make_token(user)
        send_mail(
            'Confirmation code',
            confirmation_code,
            'from@example.com',
            [email],
        )
        return resp


class AuthenticationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthenticationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if user is not None and account_activation_token.check_token(
            user=user, token=confirmation_code
        ):
            token = get_access_tokens_for_user(user)
            return Response({"token": token})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)
    # pagination_class = get_pagination_class()

    # def get_queryset(self):
    #    if self.kwargs.get('username') == 'me':
    #       username = self.request.user.username
    #    else:
    #       username = self.kwargs.get('username')
    #   queryset = get_object_or_404(User, username=username)
    #   return queryset

    def get_pagination_class(self):
        if self.action == 'list':
            return PageNumberPagination
        return None


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
    http_method_names = ['get', 'post', 'patch', 'delete']
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
