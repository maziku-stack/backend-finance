from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser or request.user.is_staff:
            return True  # Admin bypass
        allowed_roles = getattr(view, 'allowed_roles', [])
        user_groups = request.user.groups.values_list('name', flat=True)
        return any(role in user_groups for role in allowed_roles)
