from .models import Reservation

class ReservationState:
    def confirm(self, reservation):
        raise NotImplementedError

    def cancel(self, reservation):
        raise NotImplementedError

class PendingState(ReservationState):
    def confirm(self, reservation):
        reservation.state = Reservation.STATE_CONFIRMED
        reservation.save()

    def cancel(self, reservation):
        reservation.state = Reservation.STATE_CANCELLED
        reservation.save()

class ConfirmedState(ReservationState):
    def cancel(self, reservation):
        reservation.state = Reservation.STATE_CANCELLED
        reservation.save()

class CancelledState(ReservationState):
    def confirm(self, reservation):
        raise Exception("Cannot confirm a cancelled reservation.")
    
    def cancel(self, reservation):
        raise Exception("Cannot cancel an already cancelled reservation.")