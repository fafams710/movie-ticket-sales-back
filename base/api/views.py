from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from base.serializer import ProfileSerializer, ProductSerializer, UserRegistrationSerializer
from base.models import Product
from django.http import JsonResponse


# Custom Token Serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Get Profile (Authenticated Users Only)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = user.profile
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


# User Registration API
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


# Get All Products
@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# Get Single Product
@api_view(['GET'])
def get_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


# Update Product Stock
class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)  # Corrected from _id to pk
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        stock = request.data.get("stock")
        if stock is not None:
            product.stock = stock
            product.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error": "Stock value is required"}, status=status.HTTP_400_BAD_REQUEST)


# Register User (Using Correct Serializer)
@api_view(["POST"])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)  # Corrected serializer
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
