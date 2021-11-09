from rest_framework import serializers

from reviews.models import User


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
    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField(max_length=255, write_only=True)

    """def validate(self, data):
        username = data.get('username')

        if username is None:
            raise serializers.ValidationError(
                'Username is required to log in.'
            )
        if not User.objects.filter(username=username):
            raise serializers.ValidationError(
                'A user with this username was not found.'
            )
        user = User.objects.filter(username=username)
        return {
            'username': user.username,
            'token': user.token
        }   ."""
    

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']

    #def create(self, validated_data):
    #    return User.objects.create_user(**validated_data)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        role = data.get('role')

        if username is None:
            raise serializers.ValidationError(
                'Username is required.'
            )
        if email is None:
            raise serializers.ValidationError(
                'Email is required.'
            )
        if role is None:
            data.role = 'user'
        return data

    