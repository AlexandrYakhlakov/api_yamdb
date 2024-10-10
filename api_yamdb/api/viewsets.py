from rest_framework import filters, mixins, viewsets

from api.permissions import AdminOrReadOnly


class CreateListDestroyForProjectResourcesViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Cоздаём, просматриваем, удаляем."""

    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
