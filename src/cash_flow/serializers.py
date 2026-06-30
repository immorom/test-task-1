from rest_framework import serializers
from . import models

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = ['id', 'name']

class OperationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OperationType
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    operationType_name = serializers.CharField(source='operationType.name', read_only=True)

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'operationType', 'operationType_name']

class SubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = models.Subcategory
        fields = ['id', 'name', 'category', 'category_name']

class TransactionSerializer(serializers.ModelSerializer):
    status_detail         = StatusSerializer(        source = 'status',         read_only = True )
    operationType_detail  = OperationTypeSerializer( source = 'operationType',  read_only = True )
    category_detail       = CategorySerializer(      source = 'category',       read_only = True )
    subcategory_detail    = SubcategorySerializer(   source = 'subcategory',    read_only = True )

    class Meta:
        model = models.Transaction
        fields = [
            'id', 'amount', 'date', 'comment',
            'status',        'status_detail',
            'operationType', 'operationType_detail',
            'category',      'category_detail',
            'subcategory',   'subcategory_detail'
        ]

    def validate(self, attrs):
        category       = attrs.get('category')
        subcategory    = attrs.get('subcategory')
        operationType  = attrs.get('operationType')

        if category and operationType:
            if category.operationType != operationType:
                raise serializers.ValidationError({
                    "category": f"Категория '{category.name}' не принадлежит типу операции '{operationType.name}'."
                })

        if subcategory and category:
            if subcategory.category != category:
                raise serializers.ValidationError({
                    "subcategory": f"Подкатегория '{subcategory.name}' не принадлежит категории '{category.name}'."
                })

        return attrs