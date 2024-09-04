# reservations/facade.py

from .models import Flight
from .command import ReserveFlightCommand, CancelReservationCommand
from .strategies import StandardPricingStrategy

class ReservationFacade:
    def search_flights(self, query):
        if query:
            return Flight.objects.filter(destination__icontains=query)
        else:
            return Flight.objects.all()

    def reserve_flight(self, user, flight_id, seats_requested):
        command = ReserveFlightCommand(user, flight_id, seats_requested)
        return command.execute()

    def cancel_reservation(self, reservation_id):
        command = CancelReservationCommand(reservation_id)
        command.execute()

    def calculate_price(self, flight, seats_reserved, strategy):
        return strategy.calculate_price(flight, seats_reserved)
