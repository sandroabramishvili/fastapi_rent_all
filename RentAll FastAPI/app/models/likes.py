from typing import TYPE_CHECKING

from app.database import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.cars import Car


class Like(Base):
    __tablename__ = "likes"

    __table_args__ = (UniqueConstraint("user_id", "car_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="likes")
    car: Mapped["Car"] = relationship(back_populates="likes")
