from rest_framework import serializers

from reviews.models import User

from .backends import JWTAuthentication
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """
    class Meta:
        model = User
        fields = ['email', 'username']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        username = data.get('username')

        if username == 'me':
            raise serializers.ValidationError(
                'Username must not be me'
            )
        return data


class AuthenticationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    confirmation_code = serializers.CharField(max_length=255, write_only=True)
    
    def validate(self, data):
        username = data.get('username')

        if username is None:
            raise serializers.ValidationError(
                'Username is required to log in.'
            )
        user = User.objects.get(username=username)
        
        if user is None:
            raise serializers.ValidationError(
                'A user with this username was not found.'
            )

        return {
            'username': user.username,
            'token': user.token
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role', 'token']
        #read_only_fields = ('token',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if username is None:
            raise serializers.ValidationError(
                'Username is required.'
            )
        if email is None:
            raise serializers.ValidationError(
                'Email is required.'
            )
        return data

    