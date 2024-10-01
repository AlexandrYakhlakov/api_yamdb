from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, send_confirm_code

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('v1/', include('djoser.urls.jwt'))
    path('v1/auth/signup/', send_confirm_code, name='send_confirm_code')
]