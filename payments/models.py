from django.db import models
from django.conf import settings
from api.models import Order, DateStampedModel
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save

import random
import string


def generate_coupon_code(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=length))


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.timestamp)


class Discount(DateStampedModel):
    name = models.CharField(max_length=64)
    discount_percentage = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(
        max_length=15, default=generate_coupon_code, editable=False)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def expired(self):
        if self.duration is not None:
            now = datetime.now(timezone.utc)
            if now - self.created_at > self.duration:
                return True

        return False

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = generate_coupon_code()
        return super().save(*args, **kwargs)


class Refund(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return self.email
