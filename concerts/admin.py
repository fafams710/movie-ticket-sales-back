from django.contrib import admin
from concerts.models import Concert
from tickets.models import TicketType

class TicketTypeInline(admin.TabularInline):
    model = TicketType  # Use the TicketType model directly
    extra = 1  # Number of extra blank ticket types to display
    fields = ['category', 'name', 'price', 'total_quantity', 'remaining_quantity']

class ConcertAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'date', 'venue', 'created_at')
    search_fields = ('title', 'venue', 'organizer__email')
    list_filter = ('date', 'venue')
    ordering = ('-created_at',)
    inlines = [TicketTypeInline]

admin.site.register(Concert, ConcertAdmin)
