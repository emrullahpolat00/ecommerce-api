from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.models.tables import Order, OrderItem, User, Product
from app.schemas.orders import OrderCreate, OrderOut
from app.services.errors import not_found, bad_request
from app.services.validation import OrderItemIn, validate_order_items


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    user = db.get(User, payload.user_id)
    if not user:
        bad_request("user_id does not exist")

    validated_items = validate_order_items(
        OrderItemIn(product_id=it.product_id, quantity=it.quantity) for it in payload.items
    )

    for it in validated_items:
        prod = db.get(Product, it.product_id)
        if not prod:
            bad_request(f"product_id {it.product_id} does not exist")

    order = Order(user_id=payload.user_id)
    db.add(order)
    db.flush()  # order.id oluşsun

    for it in payload.items:
        db.add(OrderItem(order_id=order.id, product_id=it.product_id, quantity=it.quantity))

    db.commit()

    order = (
        db.query(Order)
        .options(selectinload(Order.items))
        .filter(Order.id == order.id)
        .first()
    )
    return order


@router.get("", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).options(selectinload(Order.items)).order_by(Order.id.asc()).all()


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).options(selectinload(Order.items)).filter(Order.id == order_id).first()
    if not order:
        not_found("Order")
    return order


@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        not_found("Order")
    db.delete(order)
    db.commit()
    return None