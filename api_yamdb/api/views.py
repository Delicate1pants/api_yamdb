from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from reviews.models import User
from .serializers import RegistrationSerializer, UserSerializer, AuthenticationSerializer
from .permissions import IsAdmin, IsAuthenticated

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .renderers import UserJSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from django.utils import six
from rest_framework.decorators import api_view
from django.core.paginator import Paginator, EmptyPage




class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()



def get_access_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    
    #renderer_classes = (UserJSONRenderer,)

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
        confirmation_code=account_activation_token.make_token(user)
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
        confirmation_code=request.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if user is not None and account_activation_token.check_token(user=user, token=confirmation_code):
            token = get_access_tokens_for_user(user)
            return Response({"token": token})
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

"""def get_pagination_class(self):
        return self.pagination_class()
    
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.get_pagination_class() is None:
                self._paginator = None
            else:
                self._paginator = self.get_pagination_class()
        return self._paginator."""

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminUser,)
    #pagination_class = get_pagination_class()

    def get_queryset(self):
        if self.kwargs.get('username') == 'me':
            username = self.request.user.username
        else:
            username = self.kwargs.get('username')
        queryset = get_object_or_404(User, username=username)
        return queryset

    def get_pagination_class(self):
        if self.action == 'list':
            return PageNumberPagination
        return None

    #def perform_create(self, serializer):
    #    serializer.is_valid(raise_exception=True)
    #    serializer.save()

"""@api_view(['GET', 'POST'])
def users_list(request, page=1):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    paginator = Paginator(users, 10)
    try:
        users = paginator.page(page)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return Response(serializer.data) 

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def users_detail(request, username):
    if username == 'me':
        username = request.user.username
    post = get_object_or_404(User, username=username)
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = UserSerializer(post, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = UserSerializer(post)
    return Response(serializer.data)."""