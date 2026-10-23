from datetime import datetime

from pydantic import BaseModel, Field


class RentalCreate(BaseModel):
    days: int = Field(ge=1, le=365)


class RentalCarOut(BaseModel):
    id: int
    brand: str
    model: str
    city: str
    price_per_day: int


class RentalOut(BaseModel):
    id: int
    days: int
    total_price: int
    created_at: datetime
    car: RentalCarOut
