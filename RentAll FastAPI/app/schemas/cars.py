from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

Transmission = Literal["automatic", "manual", "tiptronic"]

MAX_YEAR = date.today().year + 1


class CarBase(BaseModel):
    brand: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=50)
    release_year: int = Field(ge=1950, le=MAX_YEAR)
    price_per_day: int = Field(gt=0)
    capacity: int = Field(ge=1, le=20)
    transmission: Transmission
    city: str = Field(min_length=1, max_length=50)
    fuel_tank_capacity: int = Field(gt=0)


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    brand: str | None = Field(default=None, min_length=1, max_length=50)
    model: str | None = Field(default=None, min_length=1, max_length=50)
    release_year: int | None = Field(default=None, ge=1950, le=MAX_YEAR)
    price_per_day: int | None = Field(default=None, gt=0)
    capacity: int | None = Field(default=None, ge=1, le=20)
    transmission: Transmission | None = None
    city: str | None = Field(default=None, min_length=1, max_length=50)
    fuel_tank_capacity: int | None = Field(default=None, gt=0)


class CarImageOut(BaseModel):
    id: int
    url: str


class CarOwnerOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str


class CarOut(CarBase):
    id: int
    owner: CarOwnerOut
    images: list[CarImageOut] = []


class HomePageOut(BaseModel):
    popular_cars: list[CarOut]
    random_cars: list[CarOut]
