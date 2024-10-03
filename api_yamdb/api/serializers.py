from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from reviews.models import Category, Genre, Title, User, Review, Comment
from django.shortcuts import get_object_or_404


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(UnicodeUsernameValidator(),)
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class AuthUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class AuthSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(UnicodeUsernameValidator(),)
    )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Недопустимое имя для логина')
        return username


class GetTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    def validate_author(self, value):
        user = self.context['reuest'].user
        title = get_object_or_404(
            Title, id=self.context['view'].kwargs.get('title_id')
        )
        if Review.objects.filter(author=user, title=title).exists():
            raise serializers.ValidationError(
                'Оставить отзыв можно лишь один раз!'
            )
        return value

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

    def create(self, validated_data):
        """Возвращаем экземпляр объекта сериализации."""
        return Category.objects.create(**validated_data)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализации и десериализации данных, связанных с моделью Title."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        read_only_fields = ('genre', 'category',)
        model = Title
