from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Car, User
from app.schemas.cars import CarCreate, CarOut, CarUpdate
from app.security import get_current_user

router = APIRouter(prefix="/cars", tags=["Cars"])


def get_car_or_404(car_id: int, db: Session) -> Car:
    car = db.get(Car, car_id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


def check_owner(car: Car, user: User) -> None:
    if car.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You can only change your own cars")


#   /cars?city=Batumi&year_from=1995&year_to=2005&capacity=6
@router.get("", response_model=list[CarOut])
def list_cars(
    city: str | None = None,
    year_from: int | None = Query(default=None, ge=1950),
    year_to: int | None = Query(default=None, ge=1950),
    capacity: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
):
    if year_from is not None and year_to is not None and year_from > year_to:
        raise HTTPException(status_code=400, detail="year_from can't be greater than year_to")

    stmt = select(Car)

    if city is not None:
        stmt = stmt.where(func.lower(Car.city) == city.strip().lower())
    if year_from is not None:
        stmt = stmt.where(Car.release_year >= year_from)
    if year_to is not None:
        stmt = stmt.where(Car.release_year <= year_to)
    if capacity is not None:
        stmt = stmt.where(Car.capacity == capacity)

    return db.scalars(stmt.order_by(Car.id.desc())).all()


@router.post("", response_model=CarOut, status_code=status.HTTP_201_CREATED)
def create_car(
    car_data: CarCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    car = Car(**car_data.model_dump(), owner_id=current_user.id)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


@router.get("/{car_id}", response_model=CarOut)
def get_car(car_id: int, db: Session = Depends(get_db)):
    return get_car_or_404(car_id, db)


@router.patch("/{car_id}", response_model=CarOut)
def update_car(
    car_id: int,
    car_data: CarUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    car = get_car_or_404(car_id, db)
    check_owner(car, current_user)

    for field, value in car_data.model_dump(exclude_unset=True).items():
        setattr(car, field, value)

    db.commit()
    db.refresh(car)
    return car


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    car = get_car_or_404(car_id, db)
    check_owner(car, current_user)

    db.delete(car)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
