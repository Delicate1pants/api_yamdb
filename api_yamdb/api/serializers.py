from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_list_or_404
from rest_framework import fields, serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


def custom_get_rating(self, obj):
    reviews = get_list_or_404(Review, title=obj.id)
    reviews_count = len(reviews)
    scores_summ = 0
    for review in reviews:
        scores_summ += review.score
    return scores_summ // reviews_count


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
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        custom_get_rating(self, obj)


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    def get_rating(self, obj):
        custom_get_rating(self, obj)

    class Meta:
        fields = '__all__'
        model = Title


# class TitleDefault(fields.CurrentUserDefault):
#     requires_context = True

#     def __call__(self, serializer_field):
#         title_id = serializer_field.context.get('view').kwargs.get('title_id')
#         try:
#             title = Title.objects.get(pk=title_id)
#         except ObjectDoesNotExist:
#             raise serializers.ValidationError('Введите корректный title')
#         return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    # title = serializers.HiddenField(default=TitleDefault())

    # def get_title(self, obj):
    #     title_id = self.context.get('view').kwargs.get('title_id')
    #     try:
    #         title = Title.objects.get(pk=title_id)
    #     except ObjectDoesNotExist:
    #         raise serializers.ValidationError('Введите корректный title')
    #     return title

    # def validate(self, data):
    #     already_related = Review.objects.filter(
    #         author=data['author'], title=data['title']
    #     ).exists()
    #     if already_related:
    #         raise serializers.ValidationError(
    #             'Отзыв на это произведение уже существует'
    #         )
    #     return data

    def create(self, validated_data):
        title_id = self.context.get('view').kwargs.get('title_id')
        try:
            validated_data['title'] = Title.objects.get(pk=title_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Заполните поле title')
        return Review.objects.create(**validated_data)

    class Meta:
        model = Review
        exclude = ('title',)
        read_only_fields = ('id', 'author', 'pub_date')
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=['author', 'title']
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def create(self, validated_data):
        review_id = self.context.get('view').kwargs.get('review_id')
        try:
            validated_data['review'] = Comment.objects.get(pk=review_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Введите корректный review')
        return Comment.objects.create(**validated_data)

    class Meta:
        model = Comment
        exclude = ('review',)
        read_only_fields = ('id', 'author', 'pub_date')
