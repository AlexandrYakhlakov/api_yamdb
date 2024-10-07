import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters, permissions, status, viewsets
)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import AdminOrReadOnly, IsAdmin, IsInModeratorGroup
from api.serializers import (
    AuthSignupSerializer, AuthUserInfoSerializer, CategorySerializer,
    CommentSerializer, GenreSerializer, GetTokenSerializer,
    ReviewSerializer, TitleSerializer, UserSerializer
)
from api.viewsets import GenreAndCategoryCreateListDestroyViewSet
from reviews.models import Category, Genre, Review, Title, User


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    @action(
        methods=['PATCH', 'GET'],
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def auth_user_info(self, request):
        if request.method == 'GET':
            return Response(
                AuthUserInfoSerializer(instance=request.user).data,
                status=status.HTTP_200_OK
            )
        serializer = AuthUserInfoSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def auth_signup(request):
    serializer = AuthSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError as e:
        error_message = str(e)
        if 'username' in error_message:
            field = 'username'
        elif 'email' in error_message:
            field = 'email'
        else:
            field = 'unknown'
        raise ValidationError(
            {field: f'Пользователь с таким {field} уже существует.'}
        )
    user.confirmation_code = uuid.uuid4().hex
    user.save()
    send_mail(
        subject='Код подтверждения учетной записи',
        message=f'Для подтверждения учетной записи введите код:'
                f' {user.confirmation_code}',
        from_email=settings.FROM_EMAIL,
        recipient_list=(user.email,),
        fail_silently=False
    )
    return Response(
        {**serializer.validated_data},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    data = request.data
    serializer = GetTokenSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.filter(username=data['username']).first()
    if not user:
        return Response(
            dict(message='Пользователь не найден'),
            status=status.HTTP_404_NOT_FOUND
        )

    if not user.confirmation_code:
        raise ValidationError(
            dict(message='Профиль уже был подтвержден')
        )
    elif user.confirmation_code != data['confirmation_code']:
        raise ValidationError(
            dict(message='Некорректный код подтверждения')
        )
    else:
        user.confirmation_code = None
        user.save()

    token = RefreshToken.for_user(user).access_token
    return Response(
        dict(username=user.username, token=str(token)),
        status=status.HTTP_200_OK
    )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsInModeratorGroup,
    ]
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title()
        )

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsInModeratorGroup
    ]
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class TitleViewSet(viewsets.ModelViewSet):
    """Класс для выполнения операций с моделью Title.

    -в поле queryset - выбираем объект модели, с которой будет работать вьюсет;
    -в поле serializer_class - указываем, какой сериализатор будет применён
    для валидации и сериализации;
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-rating')
    serializer_class = TitleSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']


class GenreViewSet(GenreAndCategoryCreateListDestroyViewSet):
    """Класс для выполнения операций с моделью Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreAndCategoryCreateListDestroyViewSet):
    """Класс для выполнения операций с моделью Genre."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
