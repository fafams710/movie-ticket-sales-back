from django.urls import path
from .views import ConcertListView, ConcertDetailView
from tickets.views import ConcertsAPI

urlpatterns = [
    path('', ConcertListView.as_view(), name='concert-list'),
    path('<int:concert_id>/', ConcertDetailView.as_view(), name='concert-detail'),
]
