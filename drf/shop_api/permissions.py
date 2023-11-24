from rest_framework.permissions import BasePermission, SAFE_METHODS
from .enums import RoleEnum


class IsRepresentOrReadOnly(BasePermission):
    """
    The request is from users with role="represent", or is a read-only request.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.role == RoleEnum.REPRESENT
        )
