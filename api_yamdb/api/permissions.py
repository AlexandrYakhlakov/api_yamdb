from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    # def has_object_permission(self, request, view, obj):
    #     return (
    #         request.method in permissions.SAFE_METHODS
    #         or request.user.is_admin
    #     )


class AdminOrAuthorOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                obj.author == request.user
                or request.user.is_moderator
            )
        return False

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


AdminOrReadOnly = AdminOnly | ReadOnly


# class AdminOrReadOnly(AdminOnly):
#     """Проверяем пользователя.

#     Если пользовтель не админ - предоставляем только чтение.
#     """

#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or super().has_permission(request, view)
#         )

