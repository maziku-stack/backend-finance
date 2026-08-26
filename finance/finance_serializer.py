from rest_framework import serializers
from .finance_models import Category, Transaction, SavingsGoal, MonthlySummary
from users.users_models import CustomUser

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']

class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'description', 'category', 'category_id', 'amount', 'is_income']
        read_only_fields = ['id']

    def create(self, validated_data):
        category = validated_data.pop('category')
        transaction = Transaction.objects.create(category=category, **validated_data)
        return transaction

class SavingsGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsGoal
        fields = ['id', 'name', 'target_amount', 'current_amount', 'progress_percent']
        read_only_fields = ['progress_percent']

class MonthlySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlySummary
        fields = ['id', 'month', 'total_income', 'total_expenses', 'amount_saved']
        read_only_fields = ['id']
