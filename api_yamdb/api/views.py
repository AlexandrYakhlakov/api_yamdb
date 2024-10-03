from django.shortcuts import render
from rest_framework import filters, viewsets, permissions, pagination
# Create your views here.
from api.permissions import AdminOrReadOnly, IsAdminRole
from api.serializers import (
    CategorySerializer, GenreSerializer, GetTokenSerializer, TitleSerializer,
    UserSerializer, UserRegistrationSerializer
)
from api.viewsets import GenreAndCategoryCreateListDestroyViewSet
from reviews.models import Category, Genre, Title, User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminRole)
    serializer_class = UserSerializer
    pagination_class = pagination.LimitOffsetPagination
    queryset = User.objects.all()
    lookup_field = 'username'


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(
        serializer.errors,
        status=400
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    data = request.data
    serializer = GetTokenSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.filter(username=data['username'])
    if not user.exists():
        return Response(
            dict(message='Пользователь не найден'),
            status=404
        )
    user = user.first()
    if user.confirmation_code != data['confirmation_code']:
        return Response(
            dict(message='Некорректный код подтверждения'),
            status=400
        )
    token = RefreshToken.for_user(user).access_token
    return Response(
        dict(username=user.username, token=str(token)),
        status=200
    )


class TitleViewSet(viewsets.ModelViewSet):
    """Класс для выполнения операций с моделью Title.

    -в поле queryset - выбираем объект модели, с которой будет работать вьюсет;
    -в поле serializer_class - указываем, какой сериализатор будет применён
    для валидации и сериализации;
    """

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [AdminOrReadOnly]
    # Прописываем разрешенные методы:
    http_method_names = ['get', 'post', 'patch', 'delete']


class GenreViewSet(GenreAndCategoryCreateListDestroyViewSet):
    """Класс для выполнения операций с моделью Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreAndCategoryCreateListDestroyViewSet):
    """Класс для выполнения операций с моделью Genre."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

