from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Car, Like
from app.schemas.cars import HomePageOut

router = APIRouter(tags=["Home"])

HOME_LIST_SIZE = 8


@router.get("/", response_model=HomePageOut)
def home_page(db: Session = Depends(get_db)):
    popular_stmt = (
        select(Car)
        .outerjoin(Like, Like.car_id == Car.id)
        .group_by(Car.id)
        .order_by(func.count(Like.id).desc(), Car.id.desc())
        .limit(HOME_LIST_SIZE)
    )

    random_stmt = select(Car).order_by(func.random()).limit(HOME_LIST_SIZE)

    return {
        "popular_cars": db.scalars(popular_stmt).all(),
        "random_cars": db.scalars(random_stmt).all(),
    }
