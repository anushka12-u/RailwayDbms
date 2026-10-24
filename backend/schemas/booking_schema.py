from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    train_id: int
    passenger_id: int
    journey_date: date
    seat_number: int = Field(gt=0)


class BookingResponse(BookingCreate):
    booking_id: int
    booking_status: str
    booking_date: datetime
    fare: Decimal