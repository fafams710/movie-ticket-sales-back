from django.db import models
from concerts.models import Concert  # Correct reference to the Concert model

class TicketType(models.Model):
    CATEGORIES = [
        ('VIP', 'VIP (200 pax)'),
        ('LB', 'Lower Box (500 pax)'),
        ('UB', 'Upper Box (800 pax)'),
        ('GA', 'General Admission (1500 pax)')
    ]

    concert = models.ForeignKey(
        Concert,  # Reference the Concert model directly
        on_delete=models.CASCADE,
        related_name="ticket_types"  # Use related_name for reverse lookup
    )
    category = models.CharField(
        max_length=3,
        choices=CATEGORIES,
        blank=True,
        null=True
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    total_quantity = models.PositiveIntegerField(default=0)
    remaining_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.get_category_display()} tickets for {self.concert.title}" if self.category else self.name
