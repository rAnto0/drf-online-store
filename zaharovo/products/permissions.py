from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешает доступ всем пользователям для безопасных методов,
    а для методов изменения (POST, PUT, PATCH, DELETE) требует, чтобы пользователь был администратором.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS: GET, HEAD, OPTIONS – разрешены всем
        if request.method in SAFE_METHODS:
            return True
        # Для остальных методов проверяем, что пользователь аутентифицирован и является администратором
        return request.user and request.user.is_staff
