from database import get_connection


def add_passenger(passenger):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO passengers (name, age, gender, email, phone)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            passenger.name,
            passenger.age,
            passenger.gender,
            passenger.email,
            passenger.phone,
        )

        cursor.execute(query, values)
        conn.commit()

        return {
            "message": "Passenger added successfully",
            "passenger_id": cursor.lastrowid,
        }
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def get_passenger_by_id(passenger_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM passengers WHERE passenger_id = %s",
            (passenger_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_passengers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM passengers")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def update_passenger(passenger_id, passenger):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
        UPDATE passengers
        SET name = %s,
            age = %s,
            gender = %s,
            email = %s,
            phone = %s
        WHERE passenger_id = %s
        """
        values = (
            passenger.name,
            passenger.age,
            passenger.gender,
            passenger.email,
            passenger.phone,
            passenger_id,
        )

        cursor.execute(query, values)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

    return get_passenger_by_id(passenger_id)


def delete_passenger(passenger_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM passengers WHERE passenger_id = %s",
            (passenger_id,),
        )
        conn.commit()

        if cursor.rowcount == 0:
            return None

        return {"message": "Passenger deleted successfully"}
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()