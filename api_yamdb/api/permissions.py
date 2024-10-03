from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):

        return request.user.is_superuser or request.user.is_admin


class AdminOrReadOnly(permissions.BasePermission):
    """Проверяем пользователя.

    Если пользовтель не админ - предоставляем только чтение.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin)
        )

