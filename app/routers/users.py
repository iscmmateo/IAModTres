from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..deps import get_current_user
from ..schemas import UserOut
from ..models import User
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def me(current: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserOut(id=current.id, email=current.email)
