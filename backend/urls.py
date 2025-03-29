"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from tickets.views import TicketAvailabilityAPI, ReserveTicketsAPI
from orders.views import CreateOrderAPI, OrderHistoryAPI
from users.views import CustomTokenObtainPairView, RegisterView 
from tickets.views import TicketTypeListView
from tickets.views import ConcertsAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base.api.urls')),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        # Concerts
    path('api/concerts/', include('concerts.urls')),
    path("api/concerts/<int:pk>/", ConcertsAPI.as_view(), name="concert-detail"),
    # Tickets
    path('api/tickets/availability/<int:concert_id>/', 
         TicketAvailabilityAPI.as_view(), name='ticket-availability'),
    path('api/tickets/reserve/', 
         ReserveTicketsAPI.as_view(), name='reserve-tickets'),
    path('api/', include('tickets.urls')),
    path("api/ticket-types/", TicketTypeListView.as_view(), name="ticket-type-list"),
    # Orders
    path('api/orders/', CreateOrderAPI.as_view(), name='create-order'),
    path('api/orders/history/', OrderHistoryAPI.as_view(), name='order-history'),
    path("api/users/", include("users.urls")),  # Include users app URLs

    # Payments
   path('payments/', include('payments.urls')),  
]
