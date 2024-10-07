from rest_framework import filters, mixins, viewsets

from api.permissions import AdminOrReadOnly


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Cоздаём, просматриваем, удаляем."""


class GenreAndCategoryViewSet(CreateListDestroyViewSet):
    """Наследованный класс применяем к Жанрам и Категориям проекта."""

    permission_classes = [AdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
