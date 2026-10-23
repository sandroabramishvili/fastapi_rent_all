from pydantic import BaseModel


class LikeStatusOut(BaseModel):
    car_id: int
    liked: bool
    likes_count: int
