from typing import TYPE_CHECKING

from app.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.cars import Car
    from app.models.rentals import Rental
    from app.models.likes import Like


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    phone: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)

    hashed_password: Mapped[str] = mapped_column(String(255))

    cars: Mapped[list["Car"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    rentals: Mapped[list["Rental"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    likes: Mapped[list["Like"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    @property
    def liked_cars(self) -> list["Car"]:
        return [like.car for like in self.likes]
