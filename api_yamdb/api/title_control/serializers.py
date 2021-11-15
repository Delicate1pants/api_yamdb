from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import fields, serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.title_control.models import (Category, Comment, Genre, Review,
                                          Title, User)


class RegistrationSerializer(serializers.ModelSerializer):

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


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=['admin', 'moderator', 'user'],
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]


class UserpostSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]

    def validate(self, data):
        role = data.get('role')
        if role is None:
            data["role"] = 'user'
        return data


class UserpatchSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class CustomTitle(fields.CurrentUserDefault):
    requires_context = True

    def __call__(self, serializer_field):
        view = serializer_field.context.get('view')
        title_id = view.kwargs.get('title_id')
        try:
            title = Title.objects.get(pk=title_id)
        except ObjectDoesNotExist:
            raise Http404(
                'Объект не найден. '
                'Проверьте правильность написания PATH PARAMETER: review_id'
            )
        return title


class CustomReview(CustomTitle):
    def __call__(self, serializer_field):
        view = serializer_field.context.get('view')
        title_id = view.kwargs.get('title_id')
        review_id = view.kwargs.get('review_id')
        try:
            Title.objects.get(pk=title_id)
        except ObjectDoesNotExist:
            raise Http404(
                'Объект не найден. '
                'Проверьте правильность написания PATH PARAMETER: title_id'
            )
        try:
            review = Review.objects.get(pk=review_id)
        except ObjectDoesNotExist:
            raise Http404(
                'Объект не найден. '
                'Проверьте правильность написания PATH PARAMETER: review_id'
            )
        return review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=CustomTitle())

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'author', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.HiddenField(default=CustomReview())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'author', 'pub_date')
