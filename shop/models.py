import datetime

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    def get_descendants(self, include_self=True):
        descendants = set()
        categories_to_process = [self]

        while categories_to_process:
            category = categories_to_process.pop()
            if category not in descendants:
                descendants.add(category)
                categories_to_process.extend(category.subcategories.all())

        if not include_self:
            descendants.remove(self)
        return descendants

    def name_(self):
        if self.parent:
            return f'{self.parent} - {self.name}'
        return self.name

    def __str__(self):
        if self.parent:
            return f'{self.parent} - {self.name}'
        return self.name

    class Meta:
        ordering = ['id',]
        # db_table = 'category'


class Discount(models.Model):
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.discount_percentage}'

    class Meta:
        ordering = ['discount_percentage',]
        # db_table = 'discount'


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    def sell(self):
        self.stock -= 1
        self.save()

    def return_order(self):
        self.stock += 1
        self.save()

    @property
    def discounted_price(self):
        today = datetime.date.today()
        if self.discount:
            if self.discount.start_date and self.discount.start_date > today:
                return self.price
            if self.discount.end_date and self.discount.end_date < today:
                return self.price

            return self.price * (1 - self.discount.discount_percentage / 100)
        return self.price

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name', ]
        # db_table = 'product'


class Order(models.Model):
    user = models.ForeignKey(User, related_name='client', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    reserved = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    order_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def validate_reserv_sell(self):
        instance = Order.objects.get(id=self.id)
        if not self.sold and self.reserved != instance.reserved:
            if self.reserved:
                self.product.sell()
            if not self.reserved:
                self.product.return_order()
        if not self.reserved and self.sold != instance.sold:
            if self.sold:
                self.product.sell()
            if not self.sold:
                self.product.return_order()

    def save(self, *args, **kwargs):
        if not self.id:
            if self.sold or self.reserved:
                self.product.sell()
        else:
            self.validate_reserv_sell()
        if not self.order_price:
            self.order_price = self.product.discounted_price
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.sold or self.reserved:
            self.product.return_order()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Order for {self.product.name}"

    class Meta:
        ordering = ['user', ]
        # db_table = 'orders'
