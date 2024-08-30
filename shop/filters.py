import django_filters
from django.db.models import Q
from django.utils import timezone

from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        field_name='category', queryset=Category.objects.all(), method='filter_by_category')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    discount_more = django_filters.NumberFilter(method='filter_discount_more', label='Minimum Discount')

    class Meta:
        model = Product
        fields = ['discount_more', 'category', 'price_min', 'price_max']

    def filter_by_category(self, queryset, name, value):
        categories = value.get_descendants()
        return queryset.filter(category__in=categories)

    def filter_discount_more(self, queryset, name, value):
        today = timezone.now().date()
        return queryset.filter(
            Q(discount__discount_percentage__gte=value) &
            (Q(discount__start_date__lte=today) | Q(discount__start_date__isnull=True)) &
            (Q(discount__end_date__gte=today) | Q(discount__end_date__isnull=True))
        )
