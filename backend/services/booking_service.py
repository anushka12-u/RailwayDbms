from datetime import date

from mysql.connector import IntegrityError

from database import get_connection


class BookingValidationError(Exception):
    """Raised when booking input is not valid for the requested train."""


class PassengerNotFoundError(Exception):
    pass


class TrainNotFoundError(Exception):
    pass


class SeatAlreadyBookedError(Exception):
    pass


def add_booking(booking):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if booking.journey_date < date.today():
            raise BookingValidationError("Journey date cannot be in the past")
        if booking.seat_number <= 0:
            raise BookingValidationError("Seat number must be greater than zero")

        cursor.execute(
            "SELECT passenger_id FROM passengers WHERE passenger_id = %s",
            (booking.passenger_id,),
        )
        if cursor.fetchone() is None:
            raise PassengerNotFoundError("Passenger not found")

        # Lock the train row so concurrent bookings for the same train are
        # serialized before checking capacity and seat occupancy.
        cursor.execute(
            """
            SELECT train_id, total_seats
            FROM trains
            WHERE train_id = %s
            FOR UPDATE
            """,
            (booking.train_id,),
        )
        train = cursor.fetchone()
        if train is None:
            raise TrainNotFoundError("Train not found")
        if booking.seat_number > train[1]:
            raise BookingValidationError(
                "Seat number exceeds the train capacity"
            )

        cursor.execute(
            """
            SELECT booking_id
            FROM bookings
            WHERE train_id = %s
              AND journey_date = %s
              AND seat_number = %s
              AND booking_status <> 'CANCELLED'
            FOR UPDATE
            """,
            (booking.train_id, booking.journey_date, booking.seat_number),
        )
        if cursor.fetchone() is not None:
            raise SeatAlreadyBookedError("Seat is already booked")

        query = """
        INSERT INTO bookings
        (passenger_id, train_id, journey_date, seat_number)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            booking.passenger_id,
            booking.train_id,
            booking.journey_date,
            booking.seat_number,
        )

        cursor.execute(query, values)
        conn.commit()

        return {
            "message": "Booking added successfully",
            "booking_id": cursor.lastrowid,
        }
    except IntegrityError as exc:
        conn.rollback()
        # The database UNIQUE constraint remains the final concurrency guard.
        raise SeatAlreadyBookedError("Seat is already booked") from exc
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def get_booking_by_id(booking_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT b.*, t.fare
            FROM bookings b
            INNER JOIN trains t ON t.train_id = b.train_id
            WHERE b.booking_id = %s
            """,
            (booking_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_bookings():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT b.*, t.fare
            FROM bookings b
            INNER JOIN trains t ON t.train_id = b.train_id
            ORDER BY b.booking_date DESC
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_passenger_booking_history(passenger_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        SELECT b.booking_id,
               b.passenger_id,
               b.train_id,
               t.train_number,
               t.train_name,
               t.source,
               t.destination,
               b.journey_date,
               b.seat_number,
               b.booking_status,
               b.booking_date,
               t.fare
        FROM bookings b
        INNER JOIN trains t ON t.train_id = b.train_id
       INNER JOIN passengers p ON p.passenger_id = b.passenger_id
        WHERE b.passenger_id = %s
        ORDER BY b.journey_date DESC, b.booking_date DESC
        """
        cursor.execute(query, (passenger_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def update_booking(booking_id, booking):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
        UPDATE bookings
        SET passenger_id = %s,
            train_id = %s,
            journey_date = %s,
            seat_number = %s
        WHERE booking_id = %s
        """
        values = (
            booking.passenger_id,
            booking.train_id,
            booking.journey_date,
            booking.seat_number,
            booking_id,
        )

        cursor.execute(query, values)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

    return get_booking_by_id(booking_id)


def delete_booking(booking_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM bookings WHERE booking_id = %s",
            (booking_id,),
        )
        conn.commit()

        if cursor.rowcount == 0:
            return None

        return {"message": "Booking deleted successfully"}
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()