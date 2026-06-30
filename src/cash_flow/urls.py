from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'statuses',        views.StatusViewSet,        basename='status')
router.register(r'operation-types', views.OperationTypeViewSet, basename='operationtype')
router.register(r'categories',      views.CategoryViewSet,      basename='category')
router.register(r'subcategories',   views.SubcategoryViewSet,   basename='subcategory')
router.register(r'transactions',    views.TransactionViewSet,   basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]