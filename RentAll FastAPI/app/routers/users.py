from fastapi import APIRouter, Depends

from app.models import User
from app.schemas.users import UserProfileOut
from app.security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserProfileOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user
