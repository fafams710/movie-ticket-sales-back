from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
import uuid
from datetime import timedelta
from concerts.models import Concert
from tickets.models import TicketType
from .serializers import TicketTypeSerializer, ConcertSerializer
from django.http import JsonResponse

# List all TicketType objects
class TicketTypeListView(ListAPIView):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer

# API endpoint to reserve tickets
class ReserveTicketsAPI(APIView):
    @transaction.atomic
    def post(self, request):
        ticket_type_id = request.data.get('ticket_type')
        quantity = request.data.get('quantity')
        
        if not ticket_type_id or quantity is None:
            return Response({"error": "Ticket type and quantity are required"}, status=400)
        
        try:
            quantity = int(quantity)
        except ValueError:
            return Response({"error": "Quantity must be a valid number"}, status=400)
        
        try:
            ticket_type = TicketType.objects.select_for_update().get(id=ticket_type_id)
            if ticket_type.remaining_quantity < quantity:
                return Response({"error": "Not enough tickets available"}, status=400)
            
            ticket_type.remaining_quantity -= quantity
            ticket_type.save()

            reservation = {
                'reservation_id': str(uuid.uuid4()),
                'expires_at': (timezone.now() + timedelta(minutes=15)).isoformat(),
                'ticket_type': ticket_type.id,
                'quantity': quantity,
            }
            return Response(reservation)
        except TicketType.DoesNotExist:
            return Response({"error": "Invalid ticket type"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# API endpoint to check ticket availability
class TicketAvailabilityAPI(APIView):
    def get(self, request):
        ticket_types = TicketType.objects.all()
        availability = []
        for ticket in ticket_types:
            availability.append({
                'ticket_type': ticket.category,
                'available': ticket.remaining_quantity > 0,
                'remaining_quantity': ticket.remaining_quantity
            })
        return Response({"ticket_availability": availability})

# API endpoint to list concerts with their ticket types
class ConcertsAPI(APIView):
    def get(self, request):
        # Prefetch ticket types using the reverse relationship defined in your Concert model
        concerts = Concert.objects.prefetch_related("ticket_types").all()
        serializer = ConcertSerializer(concerts, many=True, context={"request": request})
        return Response(serializer.data)
