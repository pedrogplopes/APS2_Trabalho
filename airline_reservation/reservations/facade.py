from .models import Reservation, Flight
from .command import ReserveFlightCommand, CancelReservationCommand
from .states import PendingState, ConfirmedState

class ReservationFacade:
    def search_flights(self, query):
        if query:
            return Flight.objects.filter(destination__icontains=query)
        else:
            return Flight.objects.all()

    def reserve_flight(self, user, flight_id, seats_requested):
        command = ReserveFlightCommand(user, flight_id, seats_requested)
        reservation = command.execute()
        if reservation:
            return reservation
        return None

    def cancel_reservation(self, reservation_id):
        command = CancelReservationCommand(reservation_id)
        command.execute()

    def create_reservation(self, user, flight_id, seats_requested):
        flight = Flight.objects.get(id=flight_id)
        reservation = Reservation.objects.create(
            user=user,
            flight=flight,
            seats_reserved=seats_requested
        )
        reservation.state = Reservation.STATE_PENDING
        reservation.save()
        return reservation

    def calculate_price(self, flight, seats_reserved, strategy):
        return strategy.calculate_price(flight, seats_reserved)

    def confirm_reservation(self, reservation_id):
        reservation = Reservation.objects.get(id=reservation_id)
        if reservation.state == Reservation.STATE_PENDING:
            PendingState().confirm(reservation)
        elif reservation.state == Reservation.STATE_CONFIRMED:
            raise Exception("Reservation already confirmed.")

    def cancel_reservation(self, reservation_id):
        reservation = Reservation.objects.get(id=reservation_id)
        if reservation.state == Reservation.STATE_PENDING:
            PendingState().cancel(reservation)
        elif reservation.state == Reservation.STATE_CONFIRMED:
            ConfirmedState().cancel(reservation)
        elif reservation.state == Reservation.STATE_CANCELLED:
            raise Exception("Reservation already cancelled.")