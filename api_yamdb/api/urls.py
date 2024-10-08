from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet,
    ReviewViewSet, TitleViewSet, UserViewSet,
    auth_signup, get_token
)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


auth_url = [
    path('auth/signup/', auth_signup, name='auth_signup'),
    path('auth/token/', get_token, name='get_token')
]

url_v1 = [
    path('', include(router_v1.urls)),
    path('', include(auth_url))
]

urlpatterns = [
    path('v1/', include(url_v1)),
]
