from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Fix related name conflicts
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.number}"

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="")  # Default prevents migration error
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField(unique=True, null=True, blank=True) 
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    _id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0, null=True, blank=True)  # Default value set
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
