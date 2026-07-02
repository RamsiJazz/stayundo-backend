from django.contrib import admin

from django.contrib import admin
from .models import HousingCategory, ExpenseCategory

@admin.register(HousingCategory)
class HousingCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'housing_type', 'is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']

