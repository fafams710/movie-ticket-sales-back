from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('C', 'Customer'),
        ('O', 'Organizer'),
        ('A', 'Admin'),
    )
    role = models.CharField(max_length=1, choices=ROLES, default='C')
    phone = models.CharField(max_length=20, blank=True)
    email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
