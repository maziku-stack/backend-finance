from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .finance_models import Category,Transaction,SavingsGoal,MonthlySummary
from .finance_serializer import CategorySerializer,TransactionSerializer,SavingsGoalSerializer,MonthlySummarySerializer
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show only user’s transactions or all if admin
        user = self.request.user
        if user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SavingsGoalViewSet(viewsets.ModelViewSet):
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return SavingsGoal.objects.all()
        return SavingsGoal.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MonthlySummaryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MonthlySummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MonthlySummary.objects.all()
        return MonthlySummary.objects.filter(user=user)
