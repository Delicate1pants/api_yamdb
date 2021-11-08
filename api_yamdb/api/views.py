from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import User
from .serializers import RegistrationSerializer, UserSerializer, AuthenticationSerializer
from .permissions import IsAdmin, IsAuthenticated

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email')
        confirmation_code='12345'
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_mail(
            'Confirmation code',
            confirmation_code,
            'from@example.com',
            [email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthenticationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthenticationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        #serializer.is_valid(raise_exception=False)
        if serializer.is_valid(raise_exception=True):
            username = request.data.get('username')
            user = get_object_or_404(User, username=username)
            return Response({"token": user.token})
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        #serializer = PostSerializer(data=request.data)
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
"""def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)."""