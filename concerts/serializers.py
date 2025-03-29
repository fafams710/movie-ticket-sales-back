from rest_framework import serializers
from .models import Concert
from tickets.models import TicketType

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['id', 'category', 'price', 'total_quantity', 'remaining_quantity']

class ConcertSerializer(serializers.ModelSerializer):
    # This field name 'ticket_types' corresponds to the related_name in TicketType
    ticket_types = TicketTypeSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()  # Dynamically generate image URL

    class Meta:
        model = Concert
        fields = "__all__"

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.ar_model and hasattr(obj.ar_model, 'url'):
            return request.build_absolute_uri(obj.ar_model.url) if request else obj.ar_model.url
        return None
