from rest_framework import serializers
from .models import Item, Category, OrderItem, Order, DateStampedModel


class ItemSerializer(serializers.ModelSerializer):
	category_slug = serializers.SerializerMethodField()

	class Meta:
		model = Item
		fields = ('id', 'title', 'slug', 'description',
			'image', 'price', 'discount', 'count_sold',
			'category_slug', 'category', 'created_at',
			'modified_at', 'get_absolute_url')


	def get_category_slug(self, obj):
		return obj.category.slug



class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		fields = "__all__"



class OrderItemSerializer(serializers.ModelSerializer):

	class Meta:
		model = OrderItem
		fields = ("id", "created_at", "modified_at", "order_id",
				 "item", "quantity", "get_total_item_price")



class OrderSerializer(serializers.ModelSerializer):

	class Meta:
		model = Order
		fields = "__all__"