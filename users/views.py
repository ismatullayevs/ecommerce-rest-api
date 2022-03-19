from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from api.permissions import IsUser, ReadOnly
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsUserObject


class UserListAPIView(ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [AllowAny]


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsUserObject|ReadOnly]


class ProfileListAPIView(ListAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = [AllowAny]


class ProfileDetailAPIView(RetrieveUpdateAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = [IsUser|ReadOnly]