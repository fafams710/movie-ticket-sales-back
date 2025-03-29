from django.urls import path
from .views import OrderListView, CreateOrderAPI, OrderHistoryAPI

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('create/', CreateOrderAPI.as_view(), name='create-order'),
    path('history/', OrderHistoryAPI.as_view(), name='order-history'),
]
