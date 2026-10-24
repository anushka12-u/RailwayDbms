from fastapi import APIRouter, HTTPException

from schemas.passenger_schema import PassengerCreate, PassengerResponse
from services.passenger_service import (
    add_passenger,
    delete_passenger,
    get_passenger_by_id,
    get_passengers,
    update_passenger,
)

router = APIRouter(prefix="/passengers", tags=["Passengers"])


@router.get("/", response_model=list[PassengerResponse])
def get_all_passengers():
    return get_passengers()


@router.post("/")
def create_passenger(passenger: PassengerCreate):
    try:
        return add_passenger(passenger)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{passenger_id}", response_model=PassengerResponse)
def read_passenger(passenger_id: int):
    passenger = get_passenger_by_id(passenger_id)
    if passenger is None:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return passenger


@router.put("/{passenger_id}", response_model=PassengerResponse)
def update_passenger_route(passenger_id: int, passenger: PassengerCreate):
    result = update_passenger(passenger_id, passenger)
    if result is None:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return result


@router.delete("/{passenger_id}")
def delete_passenger_route(passenger_id: int):
    result = delete_passenger(passenger_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return result