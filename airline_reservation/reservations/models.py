from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_number = models.CharField(max_length=50, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateTimeField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.flight_number} - {self.origin} to {self.destination}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    reserved_on = models.DateTimeField(auto_now_add=True)
    seats_reserved = models.IntegerField()

    def __str__(self):
        return f"Reservation for {self.user.username} on flight {self.flight.flight_number}"
