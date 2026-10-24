from datetime import date

from fastapi import APIRouter, HTTPException, Query

from schemas.train_schema import TrainCreate, TrainResponse
from services.train_service import (
    add_train,
    delete_train,
    get_seat_availability,
    get_train_by_id,
    get_trains,
    search_trains,
    update_train,
)

router = APIRouter(prefix="/trains", tags=["Trains"])


@router.get("/search", response_model=list[TrainResponse])
def search_train_routes(
    source: str | None = Query(default=None, min_length=1),
    destination: str | None = Query(default=None, min_length=1),
):
    if source is None and destination is None:
        raise HTTPException(
            status_code=400,
            detail="At least one of source or destination is required",
        )
    return search_trains(source, destination)


@router.get("/{train_id}/availability")
def get_train_seat_availability(train_id: int, journey_date: date):
    availability = get_seat_availability(train_id, journey_date)
    if availability is None:
        raise HTTPException(status_code=404, detail="Train not found")
    return availability


@router.get("/", response_model=list[TrainResponse])
def get_all_trains():
    return get_trains()


@router.post("/")
def create_train(train: TrainCreate):
    try:
        train_id = add_train(train)
        return {"message": "Train added successfully", "train_id": train_id}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{train_id}", response_model=TrainResponse)
def read_train(train_id: int):
    train = get_train_by_id(train_id)
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    return train


@router.put("/{train_id}", response_model=TrainResponse)
def update_train_route(train_id: int, train: TrainCreate):
    result = update_train(train_id, train)

    if result is None:
        raise HTTPException(status_code=404, detail="Train not found")

    return result


@router.delete("/{train_id}")
def delete_train_route(train_id: int):
    result = delete_train(train_id)
    if not result:
        raise HTTPException(status_code=404, detail="Train not found")
    return result