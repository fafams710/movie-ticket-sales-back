from django.urls import path
from .views import (
    TicketTypeListView,
    ReserveTicketsAPI,
    TicketAvailabilityAPI,
    ConcertsAPI,
)

urlpatterns = [
    path('ticket-types/', TicketTypeListView.as_view(), name='ticket-type-list'),
    path('reserve-tickets/', ReserveTicketsAPI.as_view(), name='reserve-tickets'),
    path('ticket-availability/', TicketAvailabilityAPI.as_view(), name='ticket-availability'),
    path('concerts/', ConcertsAPI.as_view(), name='concerts-api'),
]
