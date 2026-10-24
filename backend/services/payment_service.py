from decimal import Decimal

from mysql.connector import IntegrityError

from database import get_connection


class PaymentNotFoundError(Exception):
    pass


class BookingNotFoundError(Exception):
    pass


class PaymentValidationError(Exception):
    pass


class DuplicateSuccessfulPaymentError(Exception):
    pass


def _get_payment(cursor, payment_id):
    cursor.execute(
        "SELECT * FROM payments WHERE payment_id = %s",
        (payment_id,),
    )
    return cursor.fetchone()


def create_payment(payment):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT booking_id, booking_status, train_id
            FROM bookings
            WHERE booking_id = %s
            FOR UPDATE
            """,
            (payment.booking_id,),
        )
        booking = cursor.fetchone()
        if booking is None:
            raise BookingNotFoundError("Booking not found")
        if booking["booking_status"] == "CANCELLED":
            raise PaymentValidationError(
                "Payments cannot be created for cancelled bookings"
            )

        cursor.execute(
            "SELECT fare FROM trains WHERE train_id = %s",
            (booking["train_id"],),
        )
        train = cursor.fetchone()
        if train is None:
            raise PaymentValidationError("The booking train no longer exists")

        requested_amount = Decimal(str(payment.amount))
        actual_fare = Decimal(str(train["fare"]))
        if requested_amount != actual_fare:
            raise PaymentValidationError(
                "Payment amount must match the train fare"
            )

        cursor.execute(
            """
            SELECT payment_id
            FROM payments
            WHERE booking_id = %s
              AND payment_status = 'SUCCESS'
            FOR UPDATE
            """,
            (payment.booking_id,),
        )
        if cursor.fetchone() is not None:
            raise DuplicateSuccessfulPaymentError(
                "A successful payment already exists for this booking"
            )

        cursor.execute(
            """
            INSERT INTO payments
                (booking_id, amount, payment_method, payment_status)
            VALUES (%s, %s, %s, 'SUCCESS')
            """,
            (payment.booking_id, actual_fare, payment.payment_method),
        )
        conn.commit()
        return _get_payment(cursor, cursor.lastrowid)
    except IntegrityError as exc:
        conn.rollback()
        raise DuplicateSuccessfulPaymentError(
            "A payment already exists for this booking"
        ) from exc
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def get_payments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM payments ORDER BY payment_date DESC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_payment_by_id(payment_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        payment = _get_payment(cursor, payment_id)
        if payment is None:
            raise PaymentNotFoundError("Payment not found")
        return payment
    finally:
        cursor.close()
        conn.close()


def get_payment_by_booking_id(booking_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM payments WHERE booking_id = %s ORDER BY payment_date DESC",
            (booking_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def update_payment_status(payment_id, payment_status):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT booking_id
            FROM payments
            WHERE payment_id = %s
            """,
            (payment_id,),
        )
        payment_reference = cursor.fetchone()
        if payment_reference is None:
            raise PaymentNotFoundError("Payment not found")

        cursor.execute(
            """
            SELECT b.booking_id, b.booking_status, t.fare
            FROM bookings b
            INNER JOIN trains t ON t.train_id = b.train_id
            WHERE b.booking_id = %s
            FOR UPDATE
            """,
            (payment_reference["booking_id"],),
        )
        booking = cursor.fetchone()
        if booking is None:
            raise BookingNotFoundError("Booking not found")

        cursor.execute(
            """
            SELECT *
            FROM payments
            WHERE payment_id = %s
            FOR UPDATE
            """,
            (payment_id,),
        )
        payment = cursor.fetchone()
        if payment is None:
            raise PaymentNotFoundError("Payment not found")
        if (
            payment["payment_status"] == "SUCCESS"
            and payment_status == "SUCCESS"
        ):
            conn.commit()
            return payment

        if payment_status == "SUCCESS":
            if booking["booking_status"] == "CANCELLED":
                raise PaymentValidationError(
                    "Payments cannot be marked successful for cancelled bookings"
                )
            if Decimal(str(payment["amount"])) != Decimal(str(booking["fare"])):
                raise PaymentValidationError(
                    "Payment amount must match the train fare"
                )

            cursor.execute(
                """
                SELECT payment_id
                FROM payments
                WHERE booking_id = %s
                  AND payment_status = 'SUCCESS'
                  AND payment_id <> %s
                FOR UPDATE
                """,
                (payment["booking_id"], payment_id),
            )
            if cursor.fetchone() is not None:
                raise DuplicateSuccessfulPaymentError(
                    "A successful payment already exists for this booking"
                )

        cursor.execute(
            """
            UPDATE payments
            SET payment_status = %s
            WHERE payment_id = %s
            """,
            (payment_status, payment_id),
        )
        conn.commit()
        return _get_payment(cursor, payment_id)
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
