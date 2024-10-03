from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, pagination
# Create your views here.
from .permissions import IsAdminRole
from .serializers import (
    UserSerializer, UserRegistrationSerializer, GetTokenSerializer,
    ReviewSerializer, CommentSerializer
)
from reviews.models import User, Review, Comment, Title
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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminRole,]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminRole,]

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])
    
    def get_queryset(self):
        return self.get_review().comments.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
        