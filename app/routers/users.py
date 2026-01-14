from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.models.tables import User
from app.schemas.users import UserCreate, UserUpdate, UserOut
from app.services.errors import not_found, bad_request

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(email=str(payload.email), full_name=payload.full_name)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        bad_request("Email already exists")
    db.refresh(user)
    return user


@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id.asc()).all()


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        not_found("User")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        not_found("User")

    if payload.full_name is not None:
        user.full_name = payload.full_name

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        not_found("User")
    db.delete(user)
    db.commit()
    return None