from rest_framework import serializers
from reviews.models import Category, Genre, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class GetTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)


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
