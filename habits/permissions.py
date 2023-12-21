from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователь может редактировать и удалять свои привычки, но может только читать
    чужие привычки. Публичные привычки можно только читать.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение всегда разрешено
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешение на редактирование или удаление для владельца привычки
        return obj.user == request.user


class CanReadPublicHabits(permissions.BasePermission):
    """
    Пользователь может видеть публичные привычки без возможности их редактировать или удалять.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return False
