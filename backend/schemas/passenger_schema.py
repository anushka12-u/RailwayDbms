from typing import Optional

from pydantic import BaseModel, Field
class PassengerCreate(BaseModel):
    name: str
    age: int=Field(gt=0,lt=120)
    gender: str
    email: Optional[str]=None
    phone: Optional[str]=None
class PassengerResponse(PassengerCreate):
    passenger_id:int