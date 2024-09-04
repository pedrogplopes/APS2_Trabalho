from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_number = models.CharField(max_length=50, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateTimeField()
    available_seats = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number} - {self.origin} to {self.destination} - ${self.price}"

class Reservation(models.Model):
    STATE_PENDING = 'pending'
    STATE_CONFIRMED = 'confirmed'
    STATE_CANCELLED = 'cancelled'

    STATE_CHOICES = [
        (STATE_PENDING, 'Pending'),
        (STATE_CONFIRMED, 'Confirmed'),
        (STATE_CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    reserved_on = models.DateTimeField(auto_now_add=True)
    seats_reserved = models.IntegerField()
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=STATE_PENDING)

    def __str__(self):
        return f"Reserva de assento para {self.user.username} no Vôo {self.flight.flight_number} - {self.get_state_display()}."