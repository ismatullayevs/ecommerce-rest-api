from datetime import datetime
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from slugify import slugify
from users.models import Address
import uuid


class DateStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Item(DateStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="product_images")
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name="items")
    price = models.DecimalField(max_digits=4, decimal_places=0)
    discount = models.ForeignKey(
        'payments.Discount', on_delete=models.SET_NULL, blank=True, null=True)
    count_sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        slug = self.slug
        if not slug:
            now = datetime.now()
            slug = self.title + "-" + now.strftime("%f")

        self.slug = slugify(slug)
        return super().save(*args, **kwargs)

    def get_item_price(self):
        if self.discount:
            if not self.discount.is_active:
                return self.price
            return (self.price * (100 - self.discount.discount_percentage) / 100)
        return self.price

    def get_absolute_url(self):
        return reverse('item_detail', args=(self.slug,))

    class Meta:
        ordering = ('-created_at', 'price')


class Category(DateStampedModel):
    name = models.CharField(max_length=32)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class OrderItem(DateStampedModel):
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.item.title

    def get_total_item_price(self):
        return self.item.get_item_price() * self.quantity


class Order(DateStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(blank=True, null=True)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    coupon = models.OneToOneField(
        'payments.Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_total_item_price()

        if self.coupon and not self.coupon.expired:
            total -= self.coupon.amount

        return total
