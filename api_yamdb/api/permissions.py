from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class AdminOrReadOnly(AdminOnly):
    """Проверяем пользователя.

    Если пользовтель не админ - предоставляем только чтение.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class AdminOrModeratorOrOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
