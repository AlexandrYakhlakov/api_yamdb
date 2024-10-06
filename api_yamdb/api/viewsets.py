from rest_framework import filters, mixins, viewsets

from api.permissions import AdminOrReadOnly


class GenreAndCategoryCreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Cоздаём, просматриваем, удаляем.

    Применяем к Жанрам и Категориям.
    """

    permission_classes = [AdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'