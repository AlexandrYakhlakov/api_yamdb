from rest_framework import filters, mixins, viewsets

from api.permissions import AdminOrReadOnly


class CreateListDestroyAdminOrReadLookupSearchFilterViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Cоздаём, просматриваем, удаляем.

    Дополниительно устанавливаем разрешение, фильтруем
    и задаем поле для поиска объектов отдельных экземпляров модели.
    """

    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
