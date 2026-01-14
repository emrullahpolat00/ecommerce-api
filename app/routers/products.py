from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.models.tables import Product, Category
from app.schemas.products import ProductCreate, ProductUpdate, ProductOut
from app.services.errors import not_found, bad_request

from app.services.validation import normalize_name, validate_non_empty, validate_price

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    cat = db.get(Category, payload.category_id)
    if not cat:
        bad_request("category_id does not exist")

    p = Product(
        name=normalize_name(validate_non_empty(payload.name, "name")),
        price=validate_price(payload.price),
        category_id=payload.category_id
    )
    db.add(p)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        bad_request("Could not create product")
    db.refresh(p)
    return p


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.id.asc()).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        not_found("Product")
    return p


@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        not_found("Product")

    if payload.category_id is not None:
        cat = db.get(Category, payload.category_id)
        if not cat:
            bad_request("category_id does not exist")
        p.category_id = payload.category_id

    if payload.name is not None:
        p.name = normalize_name(validate_non_empty(payload.name, "name"))
    if payload.price is not None:
        p.price = validate_price(payload.price)

    db.commit()
    db.refresh(p)
    return p


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        not_found("Product")
    db.delete(p)
    db.commit()
    return None