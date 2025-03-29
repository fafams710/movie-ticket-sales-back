from rest_framework import serializers
from concerts.models import Concert
from tickets.models import TicketType

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['id', 'category', 'price', 'total_quantity', 'remaining_quantity']

class ConcertSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True, read_only=True, source="ticket_types")

    class Meta:
        model = Concert
        fields = ['id', 'title', 'image_url', 'date', 'venue', 'description', 'ticket_types']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['id', 'category', 'price', 'total_quantity', 'remaining_quantity']