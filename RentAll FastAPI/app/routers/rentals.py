from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Rental, User
from app.routers.cars import get_car_or_404
from app.schemas.rentals import RentalCreate, RentalOut
from app.security import get_current_user

router = APIRouter(tags=["Rentals"])


@router.post("/cars/{car_id}/rent", response_model=RentalOut, status_code=status.HTTP_201_CREATED)
def rent_car(
    car_id: int,
    rental_data: RentalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    car = get_car_or_404(car_id, db)
    if car.owner_id == current_user.id:
        raise HTTPException(status_code=400, detail="You can't rent your own car")

    rental = Rental(
        days=rental_data.days,
        total_price=rental_data.days * car.price_per_day,
        user_id=current_user.id,
        car_id=car.id,
    )
    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental
