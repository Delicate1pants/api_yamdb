from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import six
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .permissions import IsOwnerOrStaff, IsAdmin
from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    AuthenticationSerializer,
    UserpostSerializer,
    UserpatchSerializer
)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
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
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAdmin,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserpostSerializer
        return UserSerializer

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsOwnerOrStaff]
    )
    def me(self, request):
        self.kwargs['username'] = request.user.username
        self.get_serializer = UserpatchSerializer
        if request.method == 'GET':
            return self.retrieve(request)
        elif request.method == 'PATCH':
            return self.partial_update(request)
        else:
            raise Exception('Not implemented')
