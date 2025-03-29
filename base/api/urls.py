from django.urls import path
from . import views
from .views import MyTokenObtainPairView, UserRegistrationView, ProductUpdateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Authentication & Profile
    path('profile/', views.get_profile, name='profile'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    
    # JWT Authentication
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Product Endpoints
    path('products/', views.get_products, name='products'),
    path('products/<str:pk>/', views.get_product, name='product'),  # ✅ Fixed function name
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
]
