from django.db import IntegrityError
from rest_framework import viewsets, permissions, pagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.core.mail import send_mail


from .permissions import IsAdminRole
from .serializers import (
    UserSerializer, AuthSignupSerializer, GetTokenSerializer
)
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminRole)
    serializer_class = UserSerializer
    pagination_class = pagination.LimitOffsetPagination
    queryset = User.objects.all()
    lookup_field = 'username'

    @action(
        methods=('PATCH', 'GET'),
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def auth_user_info(self, request):
        if request.method == 'GET':
            ...

        if request.method == 'PATCH':
            ...

    def perform_update(self, serializer):
        ...


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def auth_signup(request):
    serializer = AuthSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, create = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        return Response(
            dict(message='Пользователь с таким логином или email уже существует'),
            status=400
        )
    if not create:
        user.confirmation_code = 12345
        user.save()
    send_mail(
        subject='Код для входа',
        message=f'Код для входа {user.confirmation_code}',
        from_email='author@mail.ru',
        recipient_list=(user.email,),
        fail_silently=False
    )
    return Response(
        {**serializer.validated_data},
        status=200
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
