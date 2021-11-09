from django.shortcuts import get_list_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Titles, User


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
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]
        # write_only_fields = ('token',)

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)

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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitlesReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles

    def get_rating(self, obj):
        reviews = get_list_or_404(Review, title=obj.id)
        reviews_count = len(reviews)
        scores_summ = 0
        for review in reviews:
            scores_summ += review.score
        return scores_summ // reviews_count


class TitlesWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    def get_rating(self, obj):
        reviews = get_list_or_404(Review, title=obj.id)
        reviews_count = len(reviews)
        scores_summ = 0
        for review in reviews:
            scores_summ += review.score
        return scores_summ // reviews_count

    class Meta:
        fields = '__all__'
        model = Titles


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        exclude = ('title',)
        read_only_fields = ('id', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)
        read_only_fields = ('id', 'author', 'pub_date')
