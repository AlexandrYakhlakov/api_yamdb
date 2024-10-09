from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )


class AdminModerator(AdminOnly):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (
            super().has_object_permission(request, view, obj)
            or obj.author == request.user
            or request.user.is_moderator
        )


class AdminOrReadOnly(AdminOnly):
    """Проверяем пользователя.
    Если пользовтель не админ - предоставляем только чтение.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )
