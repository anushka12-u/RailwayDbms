from datetime import date, time, timedelta

from database import get_connection


def _normalize_train_times(train):
    if train is None:
        return None

    for field in ("departure_time", "arrival_time"):
        value = train.get(field)
        if isinstance(value, timedelta):
            seconds = int(value.total_seconds()) % (24 * 60 * 60)
            train[field] = time(
                hour=seconds // 3600,
                minute=(seconds % 3600) // 60,
                second=seconds % 60,
            )
    return train


def _normalize_train_rows(trains):
    return [_normalize_train_times(train) for train in trains]


def search_trains(source: str | None = None, destination: str | None = None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM trains WHERE 1 = 1"
        values = []

        if source:
            query += """
                AND (
                    train_number LIKE %s
                    OR train_name LIKE %s
                    OR source LIKE %s
                )
            """
            source_pattern = "%" + source.strip() + "%"
            values.extend([source_pattern, source_pattern, source_pattern])
        if destination:
            query += " AND destination LIKE %s"
            values.append("%" + destination.strip() + "%")

        query += " ORDER BY departure_time"
        cursor.execute(query, tuple(values))
        return _normalize_train_rows(cursor.fetchall())
    finally:
        cursor.close()
        conn.close()


def get_seat_availability(train_id: int, journey_date: date):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                t.train_id,
                t.train_name,
                t.total_seats,
                b.seat_number
            FROM trains t
            LEFT JOIN bookings b
                ON b.train_id = t.train_id
                AND b.journey_date = %s
                AND b.booking_status <> 'CANCELLED'
            WHERE t.train_id = %s
            """,
            (journey_date, train_id),
        )
        rows = cursor.fetchall()

        if not rows:
            return None

        train = rows[0]
        total_seats = train["total_seats"]
        booked_seat_set = {
            row["seat_number"]
            for row in rows
            if row["seat_number"] is not None
            and 1 <= row["seat_number"] <= total_seats
        }
        booked_seat_numbers = sorted(booked_seat_set)
        available_seat_numbers = [
            seat_number
            for seat_number in range(1, total_seats + 1)
            if seat_number not in booked_seat_set
        ]

        return {
            "train_id": train["train_id"],
            "train_name": train["train_name"],
            "journey_date": journey_date,
            "total_seats": total_seats,
            "booked_seats": len(booked_seat_numbers),
            "available_seats": len(available_seat_numbers),
            "booked_seat_numbers": booked_seat_numbers,
            "available_seat_numbers": available_seat_numbers,
        }
    finally:
        cursor.close()
        conn.close()


def add_train(train):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO trains
        (train_number, train_name, source, destination,
         departure_time, arrival_time, total_seats, fare)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            train.train_number,
            train.train_name,
            train.source,
            train.destination,
            train.departure_time,
            train.arrival_time,
            train.total_seats,
            train.fare
        )

        cursor.execute(query, values)
        conn.commit()

        return {
            "message": "Train added successfully",
            "train_id": cursor.lastrowid
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()
def get_train_by_id(train_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM trains WHERE train_id = %s"
        cursor.execute(query, (train_id,))
        train = cursor.fetchone()

        if not train:
            return None

        return _normalize_train_times(train)

    except Exception:
        raise

    finally:
        cursor.close()
        conn.close()
def get_trains():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM trains"
        cursor.execute(query)
        trains = cursor.fetchall()

        return _normalize_train_rows(trains)

    except Exception:
        raise

    finally:
        cursor.close()
        conn.close()
def update_train(train_id, train):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
        UPDATE trains
        SET train_number = %s,
            train_name = %s,
            source = %s,
            destination = %s,
            departure_time = %s,
            arrival_time = %s,
            total_seats = %s,
            fare = %s
        WHERE train_id = %s
        """

        values = (
            train.train_number,
            train.train_name,
            train.source,
            train.destination,
            train.departure_time,
            train.arrival_time,
            train.total_seats,
            train.fare,
            train_id
        )

        cursor.execute(query, values)
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

    return get_train_by_id(train_id)
def delete_train(train_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = "DELETE FROM trains WHERE train_id = %s"
        cursor.execute(query, (train_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return None

        return {"message": "Train deleted successfully"}

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()