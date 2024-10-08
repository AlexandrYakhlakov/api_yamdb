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
from api.permissions import AdminOrReadOnly, AdminOnly, AdminModerator
from api.serializers import (
    SignupSerializer, AuthUserInfoSerializer, CategorySerializer,
    CommentSerializer, GenreSerializer, GetTokenSerializer,
    ReviewSerializer, TitleSerializer, TitleCreateSerializer, UserSerializer
)
from api.utils import generate_confirmation_code
from api.viewsets import GenreAndCategoryViewSet
from reviews.models import Category, Genre, Review, Title, User
from reviews.constants import USER_PROFILE_PATH, USED_CODE_VALUE


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, AdminOnly)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    @action(
        methods=['PATCH', 'GET'],
        detail=False,
        url_path=USER_PROFILE_PATH,
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
    except IntegrityError as e:
        UserSerializer(data=request.data).is_valid(raise_exception=True)
    user.confirmation_code = generate_confirmation_code()
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
    user = get_object_or_404(User, username=data['username'])
    if user.confirmation_code == USED_CODE_VALUE:
        raise ValidationError(
            dict(message='Профиль уже был подтвержден')
        )
    elif user.confirmation_code != data['confirmation_code']:
        raise ValidationError(
            dict(message='Некорректный код подтверждения')
        )
    user.confirmation_code = USED_CODE_VALUE
    user.save()

    token = RefreshToken.for_user(user).access_token
    return Response(
        dict(username=user.username, token=str(token)),
        status=status.HTTP_200_OK
    )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, AdminModerator,
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
        AdminModerator
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
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleCreateSerializer


class GenreViewSet(GenreAndCategoryViewSet):
    """Класс для выполнения операций с моделью Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreAndCategoryViewSet):
    """Класс для выполнения операций с моделью Genre."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
