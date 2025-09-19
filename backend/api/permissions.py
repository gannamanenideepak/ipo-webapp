from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to anyone. Write actions require staff (admin).
    """
    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
