from .models import Reservation, Flight
from .states import PendingState, ConfirmedState, CancelledState

from .models import Reservation, Flight
from .states import PendingState

class ReserveFlightCommand:
    def __init__(self, user, flight_id, seats_requested):
        self.user = user
        self.flight_id = flight_id
        self.seats_requested = seats_requested

    def execute(self):
        flight = Flight.objects.get(id=self.flight_id)
        if flight.available_seats >= self.seats_requested:
            reservation = Reservation.objects.create(
                user=self.user,
                flight=flight,
                seats_reserved=self.seats_requested,
                state=Reservation.STATE_PENDING
            )
            flight.available_seats -= self.seats_requested
            flight.save()
            return reservation
        return None

class CancelReservationCommand:
    def __init__(self, reservation_id):
        self.reservation_id = reservation_id

    def execute(self):
        reservation = Reservation.objects.get(id=self.reservation_id)
        state_class = {
            Reservation.STATE_PENDING: PendingState,
            Reservation.STATE_CONFIRMED: ConfirmedState,
            Reservation.STATE_CANCELLED: CancelledState
        }[reservation.state]

        state_class().cancel(reservation)