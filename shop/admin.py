from django.contrib import admin
from .models import Category, Product, Order, Discount


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_', 'created_at', 'last_edit']
    list_display_links = ['id', 'name_']
    list_filter = ['created_at', 'last_edit']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'discount_percentage', 'start_date', 'end_date', 'created_at', 'last_edit']
    list_display_links = ['id', 'discount_percentage']
    list_filter = ['start_date', 'end_date', 'created_at', 'last_edit']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock', 'discounted_price', 'created_at', 'last_edit']
    list_display_links = ['id', 'name',]
    list_filter = ['category', 'created_at', 'last_edit']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'reserved', 'sold', 'order_price', 'created_at', 'last_edit']
    list_display_links = ['id', 'user', 'product',]
    list_filter = ['product', 'reserved', 'sold', 'order_price', 'created_at', 'last_edit']

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
