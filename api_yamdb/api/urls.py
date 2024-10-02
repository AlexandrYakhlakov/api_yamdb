from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, user_registration, get_token

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', user_registration, name='user_registration'),
    path('v1/auth/token/', get_token, name='get_token')
]