from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .finance_views import CategoryViewSet,TransactionViewSet,SavingsGoalViewSet,MonthlySummaryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'transactions', TransactionViewSet,basename='transactions')
router.register(r'savings-goals', SavingsGoalViewSet,basename='savings-goals')
router.register(r'monthly-summaries', MonthlySummaryViewSet,basename='monthly-summaries')

urlpatterns = [
    path('', include(router.urls)),
]
