from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from . import models

@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display       = ('id', 'name')
    list_display_links = ('name',)     
    search_fields      = ('name',)     

@admin.register(models.OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display       = ('id', 'name')
    list_display_links = ('name',)
    search_fields      = ('name',)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display       = ('id', 'name', 'operationType')
    list_display_links = ('name',)
    list_filter        = ('operationType',)               
    search_fields      = ('name',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('operationType')

@admin.register(models.Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display       = ('id', 'name', 'get_category', 'get_operationType')
    list_display_links = ('name',)
    list_filter        = ('category__operationType', 'category')
    search_fields      = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category__operationType')

    @admin.display(ordering='category__name', description='Категория')
    def get_category(self, obj):
        return obj.category.name

    @admin.display(ordering='category__operationType__name', description='Тип операции')
    def get_operationType(self, obj):
        return obj.category.operationType.name


class TransactionAdminForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        operationType = cleaned_data.get('operationType')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if category and operationType and category.operationType != operationType:
            raise ValidationError({
                'category': f"Категория '{category.name}' не относится к типу '{operationType.name}'."
            })

        if subcategory and category and subcategory.category != category:
            raise ValidationError({
                'subcategory': f"Подкатегория '{subcategory.name}' не относится к категории '{category.name}'."
            })

        return cleaned_data
    
@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm

    list_display       = ('id', 'date', 'amount', 'operationType', 'category', 'subcategory', 'status')
    list_display_links = ('id', 'date')
    list_filter        = ('date', 'status', 'operationType', 'category')
    search_fields      = ('comment', 'amount')
    ordering           = ('-date', '-id')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related( 'status', 'operationType', 'category', 'subcategory' )