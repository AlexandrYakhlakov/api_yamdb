from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.mixins import UserNameValidationMixin
from reviews.constants import (
    EMAIL_LENGTH, USERNAME_LENGTH
)
from reviews.models import (
    Category, Comment, Genre, Review, Title, User
)


class UserSerializer(UserNameValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class AuthUserInfoSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignupSerializer(UserNameValidationMixin, serializers.Serializer):
    email = serializers.EmailField(
        max_length=EMAIL_LENGTH,
        required=True
    )
    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True
    )


class GetTokenSerializer(UserNameValidationMixin, serializers.Serializer):
    confirmation_code = serializers.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        required=True
    )
    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        if Review.objects.filter(
            author=request.user,
            title=get_object_or_404(
                Title,
                id=self.context['view'].kwargs['title_id']
            )
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )
        return data

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'pub_date'
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализации и десериализации данных, связанных с моделью Genre."""

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализации и десериализации данных, связанных с моделью Category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка или экземляра модели Title."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = ('__all__',)


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор изменения или создания экземпляра модели Title."""

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def to_representation(self, instance):
        return TitleSerializer(instance).data
