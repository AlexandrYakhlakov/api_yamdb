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
from api.permissions import (
    AdminOrReadOnly, AdminOnly, AdminOrModeratorOrOwnerOrReadOnly
)
from api.serializers import (
    SignupSerializer, AuthUserInfoSerializer, CategorySerializer,
    CommentSerializer, GenreSerializer, GetTokenSerializer,
    ReviewSerializer, TitleSerializer, TitleWriteSerializer,
    UserSerializer,
)
from api.utils import generate_confirmation_code
from api.viewsets import ContentBaseCreateListDestroyViewSet
from reviews.models import Category, Genre, Review, Title, User

USER_EXISTS_ERROR = 'Пользователь с таким {} уже существует.'
USERNAME_FIELD_NAME = 'username'
EMAIL_FIELD_NAME = 'email'
CONFIRMATION_CODE_FIELD_NAME = 'confirmation_code'


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = USERNAME_FIELD_NAME
    filter_backends = (filters.SearchFilter,)
    search_fields = (USERNAME_FIELD_NAME,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    @action(
        methods=['PATCH', 'GET'],
        detail=False,
        url_path=settings.USER_PROFILE_PATH,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def auth_user_info(self, request):
        if request.method == 'GET':
            return Response(
                UserSerializer(instance=request.user).data,
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
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        username = serializer.validated_data[USERNAME_FIELD_NAME]
        duplicate_username = User.objects.filter(
            username=username
        ).values_list(USERNAME_FIELD_NAME).first()

        raise ValidationError(
            {
                USERNAME_FIELD_NAME: USER_EXISTS_ERROR.format(
                    USERNAME_FIELD_NAME
                )
            }
            if username == duplicate_username
            else {
                EMAIL_FIELD_NAME: USER_EXISTS_ERROR.format(EMAIL_FIELD_NAME)
            }
        )

    user.confirmation_code = generate_confirmation_code()
    user.save(update_fields=[CONFIRMATION_CODE_FIELD_NAME])
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
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    username = validated_data[USERNAME_FIELD_NAME]
    confirmation_code = validated_data[CONFIRMATION_CODE_FIELD_NAME]
    user = get_object_or_404(User, username=username)
    current_confirmation_code = user.confirmation_code

    # Обновить по пользователю confirmation_code на USED_CODE_VALUE,
    # если там еще нет этого значения
    if current_confirmation_code != settings.USED_CODE_VALUE:
        user.confirmation_code = settings.USED_CODE_VALUE
        user.save(update_fields=[CONFIRMATION_CODE_FIELD_NAME])

    if (
        current_confirmation_code == settings.USED_CODE_VALUE
        or current_confirmation_code != confirmation_code
    ):
        raise ValidationError(
            dict(
                message='Некорректный код подтверждения. Запросите новый код.'
            )
        )

    token = RefreshToken.for_user(user).access_token
    return Response(
        dict(token=str(token)),
        status=status.HTTP_200_OK
    )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        AdminOrModeratorOrOwnerOrReadOnly,
    ]
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.select_related('author').all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        AdminOrModeratorOrOwnerOrReadOnly
    ]
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.select_related('author').all()

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
    ).order_by(*Title._meta.ordering)
    serializer_class = TitleSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleWriteSerializer


class GenreViewSet(ContentBaseCreateListDestroyViewSet):
    """Класс для выполнения операций с моделью Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ContentBaseCreateListDestroyViewSet):
    """Класс для выполнения операций с моделью Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
