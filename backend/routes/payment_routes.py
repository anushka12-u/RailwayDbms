from fastapi import APIRouter, HTTPException, status

from schemas.payment_schema import (
    PaymentCreate,
    PaymentResponse,
    PaymentStatusUpdate,
)
from services.payment_service import (
    BookingNotFoundError,
    DuplicateSuccessfulPaymentError,
    PaymentNotFoundError,
    PaymentValidationError,
    create_payment,
    get_payment_by_booking_id,
    get_payment_by_id,
    get_payments,
    update_payment_status,
)

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment_route(payment: PaymentCreate):
    try:
        return create_payment(payment)
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except DuplicateSuccessfulPaymentError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except PaymentValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to create payment")


@router.get("/", response_model=list[PaymentResponse])
def get_all_payments():
    return get_payments()


@router.get("/booking/{booking_id}", response_model=list[PaymentResponse])
def get_booking_payments(booking_id: int):
    return get_payment_by_booking_id(booking_id)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int):
    try:
        return get_payment_by_id(payment_id)
    except PaymentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch("/{payment_id}/status", response_model=PaymentResponse)
def change_payment_status(payment_id: int, update: PaymentStatusUpdate):
    try:
        return update_payment_status(payment_id, update.payment_status)
    except PaymentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except DuplicateSuccessfulPaymentError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except PaymentValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to update payment")
