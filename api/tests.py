from django.test import TestCase, Client
from .models import Item, OrderItem, Category, Order
from payments.models import Discount, Coupon, Payment
from django.contrib.auth.models import User
import datetime
from datetime import timezone
from django.utils import timezone


class ItemTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Pizza")
        discount = Discount.objects.create(
            name="Qishki chegirmalar", discount_percentage=30)
        item = Item.objects.create(
            title="Pepperoni Derevyanskiy",
            description="Good pizza",
            image="Some image",
            category=category,
            price=150,
            discount=discount
        )

    def test_item(self):
        category = Category.objects.get(name="Pizza")
        item = Item.objects.get(title="Pepperoni Derevyanskiy")

        self.assertEqual(item.title, "Pepperoni Derevyanskiy")
        self.assertEqual(item.description, "Good pizza")
        self.assertEqual(item.category, category)
        self.assertEqual(item.price, 150)

    def test_get_item_price(self):
        item = Item.objects.get(title="Pepperoni Derevyanskiy")
        self.assertEqual(item.get_item_price(), 105)


class OrderItemTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Pizza")
        item = Item.objects.create(
            title="Pepperoni Derevyanskiy",
            description="Good pizza",
            image="Some image",
            category=category,
            price=150,
        )

        user = User.objects.create_user(username="dany")
        order = Order.objects.create(user=user)
        OrderItem.objects.create(order=order, item=item, quantity=3)

    def test_order_item(self):
        item = Item.objects.get(title="Pepperoni Derevyanskiy")
        order_item = OrderItem.objects.get(item=item)

        self.assertEqual(order_item.item, item)
        self.assertEqual(order_item.quantity, 3)

    def test_total_item_price(self):
        order_item = OrderItem.objects.get(
            item__title="Pepperoni Derevyanskiy")

        self.assertEqual(order_item.get_total_item_price(), 450)


class OrderTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="jimmy")
        order = Order.objects.create(user=user)

    def test_order_fields(self):
        user = User.objects.get(username="jimmy")
        order = Order.objects.get(user=user)

        self.assertEqual(order.user, user)
