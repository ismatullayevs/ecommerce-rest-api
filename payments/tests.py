from django.test import TestCase
from django.contrib.auth.models import User
from .models import Payment, Coupon, Discount, Refund
from api.models import Order
from datetime import datetime, timedelta, timezone
import time
import string


class PaymentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="daniel")
        order = Order.objects.create(user=user)
        payment = Payment.objects.create(order=order, amount=125)

    def test_payment_content(self):
        user = User.objects.get(username="daniel")
        order = Order.objects.get(user=user)
        payment = Payment.objects.get(amount=125, order=order)

        self.assertEqual(payment.order, order)
        self.assertEqual(payment.amount, 125)


class DiscountTestCase(TestCase):
    def setUp(self):
        discount = Discount.objects.create(
            name="Winter discount", discount_percentage=20)

    def test_discount(self):
        discount = Discount.objects.get(name="Winter discount")

        self.assertEqual(discount.name, "Winter discount")
        self.assertEqual(discount.discount_percentage, 20)
        self.assertTrue(discount.is_active)


class CouponTestCase(TestCase):
    def setUp(self):
        coupon = Coupon.objects.create(amount=145, duration=timedelta(hours=2))

    def test_coupon(self):
        c = Coupon.objects.get(amount=145)
        self.assertEqual(c.amount, 145)
        self.assertEqual(c.duration, timedelta(hours=2))

    def test_coupon_code(self):
        c = Coupon.objects.get(amount=145)
        allowed_chars = string.ascii_uppercase + string.ascii_lowercase
        for char in c.code:
            self.assertIn(char, allowed_chars)

    def test_coupon_not_expired(self):
        c = Coupon.objects.get(amount=145)
        self.assertFalse(c.expired)
        c2 = Coupon.objects.create(amount=140)
        self.assertFalse(c.expired)

    def test_coupon_is_expired(self):
        c3 = Coupon.objects.create(amount=140, duration=timedelta(seconds=0))
        self.assertTrue(c3.expired)

    def test_coupon_representation(self):
        c = Coupon.objects.get(amount=145)
        self.assertEqual(c.__str__(), c.code)


class RefundTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="daniel")
        order = Order.objects.create(user=user)
        refund = Refund.objects.create(
            order=order, reason="Broken package", email="example@gmail.com")

    def test_refund_contents(self):
        order = Order.objects.get(user__username="daniel")
        refund = Refund.objects.get(reason="Broken package")

        self.assertEqual(refund.order, order)
        self.assertEqual(refund.reason, "Broken package")
        self.assertEqual(refund.email, "example@gmail.com")
