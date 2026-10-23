from pydantic import BaseModel, EmailStr, Field

from app.schemas.cars import CarOut
from app.schemas.rentals import RentalOut

PHONE_PATTERN = r"^\+?\d{9,15}$"


class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone: str = Field(pattern=PHONE_PATTERN, max_length=20)
    email: EmailStr = Field(max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)


class UserLogin(BaseModel):
    phone: str = Field(pattern=PHONE_PATTERN, max_length=20)
    password: str


class UserOut(UserBase):
    id: int


class UserProfileOut(UserOut):
    rentals: list[RentalOut] = []
    liked_cars: list[CarOut] = []
    cars: list[CarOut] = []


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
