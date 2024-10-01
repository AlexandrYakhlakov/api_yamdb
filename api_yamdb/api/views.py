from django.shortcuts import render
from rest_framework import viewsets, permissions, pagination
# Create your views here.
from .permissions import IsAdminRole
from .serializers import UserSerializer
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated, IsAdminRole)
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    pagination_class = pagination.LimitOffsetPagination
    queryset = User.objects.all()
    lookup_field = 'username'
