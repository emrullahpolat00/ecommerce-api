from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.models.tables import Review, User, Product
from app.schemas.reviews import ReviewCreate, ReviewUpdate, ReviewOut
from app.services.errors import not_found, bad_request

from app.services.validation import validate_rating

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("", response_model=ReviewOut, status_code=201)
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)):
    if not db.get(User, payload.user_id):
        bad_request("user_id does not exist")
    if not db.get(Product, payload.product_id):
        bad_request("product_id does not exist")

    r = Review(
        user_id=payload.user_id,
        product_id=payload.product_id,
        rating=validate_rating(payload.rating),
        comment=payload.comment,
    )
    db.add(r)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        bad_request("User already reviewed this product")
    db.refresh(r)
    return r


@router.get("", response_model=list[ReviewOut])
def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).order_by(Review.id.asc()).all()


@router.get("/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    r = db.get(Review, review_id)
    if not r:
        not_found("Review")
    return r


@router.put("/{review_id}", response_model=ReviewOut)
def update_review(review_id: int, payload: ReviewUpdate, db: Session = Depends(get_db)):
    r = db.get(Review, review_id)
    if not r:
        not_found("Review")

    if payload.rating is not None:
        r.rating = validate_rating(payload.rating)
    if payload.comment is not None:
        r.comment = payload.comment

    db.commit()
    db.refresh(r)
    return r


@router.delete("/{review_id}", status_code=204)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    r = db.get(Review, review_id)
    if not r:
        not_found("Review")
    db.delete(r)
    db.commit()
    return None