from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Item, Category, OrderItem, Order
from .serializers import ItemSerializer, CategorySerializer, OrderItemSerializer, OrderSerializer
from .paginators import CursorSetPagination
from .permissions import ReadOnly, IsUser, IsOrderUser
from api import permissions


class CategoryListAPIView(ListCreateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [IsAdminUser|ReadOnly]


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	lookup_field = 'slug'
	permission_classes = [IsAdminUser|ReadOnly]


class ItemListAPIView(ListCreateAPIView):
	serializer_class = ItemSerializer
	pagination_class = CursorSetPagination
	permission_classes = [IsAdminUser|ReadOnly]

	def get_queryset(self):
		category_slug = self.request.GET.get('category_slug')
		queryset = Item.objects.all()
		if category_slug:
			queryset = queryset.filter(category__slug=category_slug)

		return queryset


class ItemDetailAPIView(RetrieveUpdateDestroyAPIView):
	queryset = Item.objects.all()
	serializer_class = ItemSerializer
	lookup_field = 'slug'
	permission_classes = [IsAdminUser|ReadOnly]


class OrderItemDetailAPIView(RetrieveUpdateDestroyAPIView):
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer
	permission_classes = [IsOrderUser]


class OrderItemListCreateAPIView(ListCreateAPIView):
	serializer_class = OrderItemSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = OrderItem.objects.filter(order__user=self.request.user)
		order_id = self.request.GET.get('category_id')
		if order_id:
			queryset = queryset.filter(order_id=order_id)

		return queryset


	def create(self, serializer):
		serializer = self.get_serializer(data=self.request.data)
		serializer.is_valid(raise_exception=True)

		order, created = Order.objects.get_or_create(user=self.request.user, ordered=False)
		item = serializer.validated_data.get('item')
		order_items = order.items.all()
		order_item_qs = order_items.filter(item=item)
		if order_item_qs.exists():
			return Response({'detail': 'This item is already in your cart'}, status=status.HTTP_400_BAD_REQUEST)

		serializer.save(order=order)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderListAPIView(ListAPIView):
	serializer_class = OrderSerializer
	permissions_classes = [IsAuthenticated]
	
	def get_queryset(self):
		queryset = Order.objects.filter(user=self.request.user)
		return queryset


class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = [IsUser]