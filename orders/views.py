import qrcode
from io import BytesIO
from django.core.files import File
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer
from tickets.models import TicketType

class CreateOrderAPI(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can create orders

    @transaction.atomic
    def post(self, request):
        print("Received order request:", request.data)  # Debugging

        ticket_type_id = request.data.get('ticket_type')
        quantity = request.data.get('quantity')

        if not ticket_type_id or not quantity:
            return Response({"error": "ticket_type and quantity are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ticket_type = TicketType.objects.get(id=ticket_type_id)
        except TicketType.DoesNotExist:
            return Response({"error": "Ticket type not found"}, status=status.HTTP_404_NOT_FOUND)

        total_price = ticket_type.price * int(quantity)

        # Create the order
        order = Order.objects.create(
            user=request.user,
            ticket_type=ticket_type,
            quantity=quantity,
            total_price=total_price,
            payment_intent_id=request.data.get('payment_intent_id'),
        )

        print("Order created:", order)  # Debugging

        # Generate QR code
        qr = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4
        )
        qr.add_data(f"ORDER:{order.id}:{request.user.email}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        order.qr_code.save(f'qrcode_{order.id}.png', File(buffer))

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderHistoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
