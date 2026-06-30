from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from . import models, serializers

class StatusViewSet(viewsets.ModelViewSet):
    queryset         = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer


class OperationTypeViewSet(viewsets.ModelViewSet):
    queryset         = models.OperationType.objects.all()
    serializer_class = serializers.OperationTypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset         = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['operationType']


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset         = models.Subcategory.objects.all()
    serializer_class = serializers.SubcategorySerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['category']


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = models.Transaction.objects.select_related(
        'status', 'operationType', 'category', 'subcategory'
    ).all()
    
    serializer_class = serializers.TransactionSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = {
        'status'        : ['exact'],
        'operationType' : ['exact'],
        'category'      : ['exact'],
        'subcategory'   : ['exact'],
        
        'date' : ['gte', 'lte', 'exact'], 
    }
    
    search_fields = ['comment']
    
    ordering_fields = ['date', 'amount']
