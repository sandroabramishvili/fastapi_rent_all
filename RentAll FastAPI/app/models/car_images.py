from typing import TYPE_CHECKING

from app.database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.cars import Car


class CarImage(Base):
    __tablename__ = "car_images"

    id: Mapped[int] = mapped_column(primary_key=True)

    url: Mapped[str] = mapped_column(String(255))

    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id", ondelete="CASCADE"))

    car: Mapped["Car"] = relationship(back_populates="images")
