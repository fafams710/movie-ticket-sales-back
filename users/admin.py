from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # The fields to be used in displaying the CustomUser model
    list_display = ('username', 'email', 'role', 'phone', 'email_verified', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    
    # Fields to be displayed in the detail view
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'email_verified', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields to display in the admin add/edit form
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'role')}),
    )
    
    # Define the ordering of the CustomUser model in the admin list view
    ordering = ('username',)

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
