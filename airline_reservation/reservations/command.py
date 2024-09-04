# reservations/commands.py

from abc import ABC, abstractmethod
from .models import Flight, Reservation

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class ReserveFlightCommand(Command):
    def __init__(self, user, flight_id, seats_requested):
        self.user = user
        self.flight_id = flight_id
        self.seats_requested = seats_requested

    def execute(self):
        flight = Flight.objects.get(id=self.flight_id)
        if self.seats_requested <= flight.available_seats:
            Reservation.objects.create(
                user=self.user,
                flight=flight,
                seats_reserved=self.seats_requested
            )
            flight.available_seats -= self.seats_requested
            flight.save()
            return True
        return False

class CancelReservationCommand(Command):
    def __init__(self, reservation_id):
        self.reservation_id = reservation_id

    def execute(self):
        reservation = Reservation.objects.get(id=self.reservation_id)
        flight = reservation.flight
        flight.available_seats += reservation.seats_reserved
        flight.save()
        reservation.delete()
