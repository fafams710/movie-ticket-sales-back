# payments/views.py
import json
import requests
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order
from django.shortcuts import render
from django.http import JsonResponse
from .utils import send_ticket_email


# PayPal API Configuration
PAYPAL_CLIENT_ID = settings.PAYPAL_CLIENT_ID
PAYPAL_SECRET = settings.PAYPAL_SECRET
PAYPAL_API_BASE = 'https://api-m.sandbox.paypal.com'  # Change to live for production


def get_paypal_access_token():
    """Retrieve PayPal access token"""
    auth_response = requests.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        data={'grant_type': 'client_credentials'}
    )
    if auth_response.status_code == 200:
        return auth_response.json()['access_token']
    else:
        raise Exception("Unable to get PayPal access token")


class CreatePayPalOrder(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        if amount is None:
            return Response({"error": "Amount not provided"}, status=400)

        access_token = get_paypal_access_token()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        # Create a PayPal order
        order_data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "PHP",
                        "value": str(amount)
                    }
                }
            ]
        }

        response = requests.post(
            f"{PAYPAL_API_BASE}/v2/checkout/orders",
            headers=headers,
            json=order_data
        )

        if response.status_code == 201:
            order_info = response.json()
            return Response({"id": order_info['id'], "status": order_info['status']})
        else:
            return Response({"error": "Error creating PayPal order"}, status=response.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class PayPalWebhookAPI(APIView):
    def post(self, request):
        payload = request.body
        headers = request.META
        event_data = json.loads(payload)

        # Verify the webhook event (optional: you can implement a signature verification here)
        event_type = event_data.get('event_type', '')

        if event_type == 'CHECKOUT.ORDER.APPROVED':
            order_id = event_data['resource']['id']

            try:
                # Find the order using the order_id
                order = Order.objects.get(payment_intent_id=order_id)
                # Update order status to 'paid'
                order.status = 'paid'
                order.save()

                # Send ticket email
                ticket_info = {
                    "user_name": order.user.get_full_name(),
                    "user_email": order.user.email,
                    "Concert_name": "Dune: Part Two",  # Replace with dynamic movie name
                    "showtime": "March 30, 2025 - 7:00 PM"  # Replace with dynamic time
                }
                send_ticket_email(ticket_info["user_email"], ticket_info)

            except Order.DoesNotExist:
                return Response({'error': 'Order not found'}, status=404)

        return Response(status=200)


def payment_success(request):
    """Handles successful PayPal payments and sends a ticket email."""
    ticket_info = {
        "user_name": request.user.get_full_name(),
        "user_email": request.user.email,
        "Concert_name": "Dune: Part Two",
        "showtime": "March 30, 2025 - 7:00 PM"
    }

    # Send the email with the ticket and QR code
    send_ticket_email(ticket_info["user_email"], ticket_info)

    return JsonResponse({"message": "Payment successful! Ticket sent to email."})
