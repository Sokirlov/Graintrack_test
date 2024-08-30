from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.views import ProductsView, CategoryView, OrderView

router = DefaultRouter()
router.register('categorys', CategoryView, basename='categorys')
router.register('products', ProductsView, basename='products')
router.register('orders', OrderView, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
