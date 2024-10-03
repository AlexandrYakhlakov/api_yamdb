from django.urls import include, path
from rest_framework import routers

from .views import (
    UserViewSet,
    user_registration,
    get_token,
    ReviewViewSet,
    CommentViewSet,
)

router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet, basename="users")
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", user_registration, name="user_registration"),
    path("v1/auth/token/", get_token, name="get_token"),
]
