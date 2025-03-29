# payments/urls.py
from django.urls import path
from .views import CreatePayPalOrder, PayPalWebhookAPI, payment_success

urlpatterns = [
    path('create-paypal-order/', CreatePayPalOrder.as_view(), name='create-paypal-order'),
    path('paypal-webhook/', PayPalWebhookAPI.as_view(), name='paypal-webhook'),
    path('payment-success/', payment_success, name='payment-success'),
]
