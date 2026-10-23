from datetime import datetime
from typing import TYPE_CHECKING

from app.database import Base
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.cars import Car


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True)
    days: Mapped[int] = mapped_column()

    total_price: Mapped[int] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="rentals")
    car: Mapped["Car"] = relationship(back_populates="rentals")
