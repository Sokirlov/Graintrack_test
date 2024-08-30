from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from Graintrack_test.permissions import IsStaffOrReadOnly
from .filters import ProductFilter
from .models import Product, Category, Discount, Order
from .serializers import ProductSerializer, CategorySerializer, ProductUpdateSerializer, OrderSerializer, \
    OrderUpdateSerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer
    http_method_names = ['get',]


class DiscountView(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]


class ProductsView(viewsets.ModelViewSet):
    queryset = Product.objects.filter(stock__gt=0)
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return super().get_serializer_class()


class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'product__category': ['exact'],
        'sold': ['exact'],
        'reserved': ['exact'],
        'created_at': ['gte', 'lte'],
    }
    http_method_names = ['get', 'post', 'put']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
