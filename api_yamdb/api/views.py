from django.shortcuts import render
from rest_framework import viewsets, permissions, pagination
# Create your views here.
from .permissions import IsAdminRole
from .serializers import UserSerializer, SendConfirmCodeSerializer
from reviews.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated, IsAdminRole)
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    pagination_class = pagination.LimitOffsetPagination
    queryset = User.objects.all()
    lookup_field = 'username'


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_confirm_code(request):
    # breakpoint()
    serializer = SendConfirmCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(
        serializer.errors,
        status=400
    )