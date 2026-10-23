from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Like, User
from app.routers.cars import get_car_or_404
from app.schemas.likes import LikeStatusOut
from app.security import get_current_user

router = APIRouter(tags=["Likes"])


def find_like(car_id: int, user_id: int, db: Session) -> Like | None:
    return db.scalar(select(Like).where(Like.car_id == car_id, Like.user_id == user_id))


def like_status(car_id: int, liked: bool, db: Session) -> LikeStatusOut:
    likes_count = db.scalar(select(func.count(Like.id)).where(Like.car_id == car_id))
    return LikeStatusOut(car_id=car_id, liked=liked, likes_count=likes_count)


@router.post("/cars/{car_id}/like", response_model=LikeStatusOut)
def like_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_car_or_404(car_id, db)
    if find_like(car_id, current_user.id, db) is None:
        db.add(Like(car_id=car_id, user_id=current_user.id))
        db.commit()
    return like_status(car_id, True, db)


@router.delete("/cars/{car_id}/like", response_model=LikeStatusOut)
def unlike_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_car_or_404(car_id, db)
    like = find_like(car_id, current_user.id, db)
    if like is not None:
        db.delete(like)
        db.commit()
    return like_status(car_id, False, db)
