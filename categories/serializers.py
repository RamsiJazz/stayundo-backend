#categories/serializers.py
from rest_framework import serializers
from .models import HousingCategory, ExpenseCategory


class HousingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingCategory
        fields = ['id', 'name', 'slug', 'housing_type', 'tagline', 'image', 'order']


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'slug', 'image', 'description', 'order']


