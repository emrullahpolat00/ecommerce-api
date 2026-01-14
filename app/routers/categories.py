from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.models.tables import Category
from app.schemas.categories import CategoryCreate, CategoryUpdate, CategoryOut
from app.services.errors import not_found, bad_request

from app.services.validation import normalize_name, validate_non_empty

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=CategoryOut, status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    cat = Category(name=normalize_name(validate_non_empty(payload.name, "name")))
    db.add(cat)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        bad_request("Category name already exists")
    db.refresh(cat)
    return cat


@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.id.asc()).all()


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.get(Category, category_id)
    if not cat:
        not_found("Category")
    return cat


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    cat.name = normalize_name(validate_non_empty(payload.name, "name"))
    if not cat:
        not_found("Category")

    if payload.name is not None:
        cat.name = payload.name.strip()
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            bad_request("Category name already exists")
    else:
        db.commit()

    db.refresh(cat)
    return cat


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.get(Category, category_id)
    if not cat:
        not_found("Category")
    db.delete(cat)
    db.commit()
    return None