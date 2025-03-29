from rest_framework import serializers
from .models import Order
from tickets.models import TicketType

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['id', 'category', 'price', 'total_quantity', 'remaining_quantity']

class OrderSerializer(serializers.ModelSerializer):
    ticket_type = TicketTypeSerializer(read_only=True)  # Nested serializer

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'ticket_type', 'quantity', 'total_price', 
            'status', 'payment_intent_id', 'qr_code', 'created_at'
        ]
        read_only_fields = ['total_price', 'status', 'created_at']
