from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

from reviews.models import User
from .serializers import RegistrationSerializer, UserSerializer, AuthenticationSerializer
from .permissions import IsAdmin, IsOwner
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from django.utils import six
from rest_framework import generics
#from rest_framework.decorators import api_view




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


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)


    def get_object(self):
        if self.kwargs.get('username', None) == 'me':
            self.kwargs['username'] = self.request.user.username
        return super(UserDetailAPIView, self).get_object()


    def update(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

