from typing import TYPE_CHECKING

from app.database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.car_images import CarImage
    from app.models.rentals import Rental
    from app.models.likes import Like


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)

    brand: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    release_year: Mapped[int] = mapped_column()
    price_per_day: Mapped[int] = mapped_column()
    capacity: Mapped[int] = mapped_column()
    transmission: Mapped[str] = mapped_column(String(20))
    city: Mapped[str] = mapped_column(String(50))
    fuel_tank_capacity: Mapped[int] = mapped_column()

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    owner: Mapped["User"] = relationship(back_populates="cars")

    images: Mapped[list["CarImage"]] = relationship(back_populates="car", cascade="all, delete-orphan")
    rentals: Mapped[list["Rental"]] = relationship(back_populates="car", cascade="all, delete-orphan")
    likes: Mapped[list["Like"]] = relationship(back_populates="car", cascade="all, delete-orphan")
