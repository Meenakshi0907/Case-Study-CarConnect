class ReservationException(Exception):
    def __init__(self, message="Error in processing the reservation."):
        super().__init__(message)
