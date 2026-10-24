from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


PaymentMethod = Literal["UPI", "CARD", "NET_BANKING", "CASH"]
PaymentStatus = Literal["PENDING", "SUCCESS", "FAILED", "REFUNDED"]


class PaymentCreate(BaseModel):
    booking_id: int
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    payment_method: PaymentMethod


class PaymentStatusUpdate(BaseModel):
    payment_status: PaymentStatus


class PaymentResponse(BaseModel):
    payment_id: int
    booking_id: int
    amount: Decimal
    payment_method: str | None
    payment_status: str
    payment_date: datetime
