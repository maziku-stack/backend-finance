from rest_framework import viewsets, permissions
from .users_models import CustomUser
from .users_serializer import UserSerializer, UserCreateSerializer
from .permissions import RolePermission

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, RolePermission]
    allowed_roles = ['admin']  # Only admin can manage users

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
