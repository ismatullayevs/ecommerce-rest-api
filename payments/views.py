from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Payment
from .serializers import PaymentSerializer
from django.core.mail import send_mail
from django.conf import settings


class PaymentListView(ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.filter(order__user=self.request.user)
        return queryset
