from django.urls import path
from . import views
from users.views import UserListAPIView, UserDetailAPIView, ProfileListAPIView, ProfileDetailAPIView
from payments.views import PaymentListView

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view(), name="category_list"),
    path('categories/<slug>/', views.CategoryDetailAPIView.as_view(),
         name="category_detail"),
    path('products/', views.ItemListAPIView.as_view(), name="item_list"),
    path('products/<slug>/', views.ItemDetailAPIView.as_view(), name="item_detail"),
    path('order-items/', views.OrderItemListCreateAPIView.as_view(),
         name="order_item_list"),
    path('order-items/<pk>/', views.OrderItemDetailAPIView.as_view(),
         name="order_item_detail"),
    path('orders/', views.OrderListAPIView.as_view(), name="order_list"),
    path('orders/<pk>/', views.OrderDetailAPIView.as_view(), name="order_detail"),

    path('payments/', PaymentListView.as_view(), name="payment_list"),

    path('users/', UserListAPIView.as_view(), name="user_list"),
    path('users/<pk>/', UserDetailAPIView.as_view(), name="user_detail"),
    path('profiles/', ProfileListAPIView.as_view(), name="profile_list"),
    path('profiles/<pk>/', ProfileDetailAPIView.as_view(), name="profile_detail")
]
