from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Concert
from .serializers import ConcertSerializer
import logging

logger = logging.getLogger(__name__)

# List all concerts, prefetching the related ticket types.
class ConcertListView(ListAPIView):
    queryset = Concert.objects.prefetch_related("ticket_types").all()
    serializer_class = ConcertSerializer

# Retrieve a specific concert with its ticket types.
class ConcertDetailView(APIView):
    def get(self, request, concert_id):
        concert = get_object_or_404(Concert.objects.prefetch_related("ticket_types"), id=concert_id)
        serializer = ConcertSerializer(concert, context={"request": request})
        return Response(serializer.data)

# Alternative API view that supports optional pk
class ConcertAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                concert = Concert.objects.prefetch_related("ticket_types").get(id=pk)
                serializer = ConcertSerializer(concert, context={"request": request})
                return Response(serializer.data)
            except Concert.DoesNotExist:
                return Response({"error": "Concert not found"}, status=404)
        else:
            concerts = Concert.objects.prefetch_related("ticket_types").all()
            serializer = ConcertSerializer(concerts, many=True, context={"request": request})
            return Response(serializer.data)
