# payments/views.py
import stripe
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order
from django.shortcuts import render
from django.http import JsonResponse
from .utils import send_ticket_email

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntent(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        if amount is None:
            return Response({"error": "Amount not provided"}, status=400)

        # Convert amount to cents (Stripe expects the amount in the smallest currency unit)
        amount_in_cents = int(amount * 100)

        try:
            # Create a payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency='php',
            )
            return Response({'clientSecret': intent.client_secret}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentWebhookAPI(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            # Verify the webhook signature
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            # Invalid payload
            return Response(status=400)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return Response(status=400)

        # Handle the event
        if event.get('type') == 'payment_intent.succeeded':
            payment_intent = event['data']['object']

            try:
                # Find the order using the payment_intent_id
                order = Order.objects.get(payment_intent_id=payment_intent['id'])
                # Update order status to 'paid'
                order.status = 'paid'
                order.save()
            except Order.DoesNotExist:
                return Response({'error': 'Order not found'}, status=404)

        return Response(status=200)

def payment_success(request):
    """Handles successful payments and sends a ticket email."""
    # Example ticket info (replace with actual data from your system)
    ticket_info = {
        "user_name": request.user.get_full_name(),
        "user_email": request.user.email,
        "movie_name": "Dune: Part Two",
        "seat_number": "A12",
        "showtime": "March 30, 2025 - 7:00 PM"
    }

    # Send the email with the ticket and QR code
    send_ticket_email(ticket_info["user_email"], ticket_info)

    return JsonResponse({"message": "Payment successful! Ticket sent to email."})