from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    allowed_roles: set[str] = set()

    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False

        allowed_roles = getattr(view, "allowed_roles", self.allowed_roles)
        if not allowed_roles:
            return True

        return getattr(user, "role", None) in allowed_roles
