from datetime import time

from pydantic import BaseModel, Field
class Train(BaseModel):
    train_number: str
    train_name: str
    source: str
    destination: str
    departure_time: time
    arrival_time: time
    total_seats: int=Field(gt=0)
    fare:float=Field(gt=0)


TrainCreate = Train


class TrainResponse(TrainCreate):
    train_id: int
   