from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import (
    Category, Comment, Genre, Review, Title, User
)
from reviews.validators import validate_username


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserSerializer(BaseUserSerializer):
    ...


class AuthUserInfoSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        read_only_fields = ('role',)


class AuthSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=User.EMAIL_LENGTH,
        required=True
    )
    username = serializers.CharField(
        max_length=User.USERNAME_LENGTH,
        required=True,
        validators=(validate_username,)
    )


class GetTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(
        max_length=User.USERNAME_LENGTH,
        required=True,
        validators=(validate_username,)
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        if request.method == 'POST':
            if Review.objects.filter(
                author=request.user,
                title=get_object_or_404(
                    Title,
                    id=title_id
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

    def create(self, validated_data):
        """Возвращаем экземпляр объекта сериализации."""
        return Genre.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализации и десериализации данных, связанных с моделью Category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериализации и десериализации данных, связанных с моделью Title."""
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )
        read_only_fields = ('genre', 'category',)
        model = Title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method in ['PATCH', 'POST']:
            self.fields['category'] = serializers.SlugRelatedField(
                slug_field='slug',
                queryset=Category.objects.all()
            )
            self.fields['genre'] = serializers.SlugRelatedField(
                slug_field='slug',
                queryset=Genre.objects.all(),
                many=True
            )
        elif self.context['request'].method == 'GET':
            self.fields['category'] = CategorySerializer()
            self.fields['genre'] = GenreSerializer(many=True)
