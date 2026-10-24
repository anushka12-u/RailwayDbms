from fastapi import APIRouter, HTTPException, status

from schemas.booking_schema import BookingCreate, BookingResponse
from services.booking_service import (
    BookingValidationError,
    PassengerNotFoundError,
    SeatAlreadyBookedError,
    TrainNotFoundError,
    add_booking,
    delete_booking,
    get_booking_by_id,
    get_bookings,
    get_passenger_booking_history,
    update_booking,
)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/", response_model=list[BookingResponse])
def get_all_bookings():
    return get_bookings()


@router.get(
    "/passenger/{passenger_id}",
    response_model=list[BookingResponse],
)
def get_passenger_history(passenger_id: int):
    return get_passenger_booking_history(passenger_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate):
    try:
        return add_booking(booking)
    except PassengerNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except TrainNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except BookingValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except SeatAlreadyBookedError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to create booking",
        )


@router.get("/{booking_id}", response_model=BookingResponse)
def read_booking(booking_id: int):
    booking = get_booking_by_id(booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking_route(booking_id: int, booking: BookingCreate):
    result = update_booking(booking_id, booking)
    if result is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return result


@router.delete("/{booking_id}")
def delete_booking_route(booking_id: int):
    result = delete_booking(booking_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return result