from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.services.errors import bad_request


@dataclass(frozen=True)
class OrderItemIn:
    product_id: int
    quantity: int


def normalize_name(name: str) -> str:
    """Boşlukları düzeltir, baş/son boşlukları kırpar."""
    return " ".join(name.strip().split())


def validate_non_empty(value: str, field: str) -> str:
    """Boş/space stringleri engeller."""
    v = value.strip()
    if not v:
        bad_request(f"{field} must not be empty")
    return v


def validate_price(price: float) -> float:
    """Fiyat > 0 olmalı."""
    if price <= 0:
        bad_request("price must be > 0")
    return price


def validate_rating(rating: int) -> int:
    """Rating 1..5 aralığında olmalı."""
    if rating < 1 or rating > 5:
        bad_request("rating must be between 1 and 5")
    return rating


def validate_order_items(items: Iterable[OrderItemIn]) -> list[OrderItemIn]:
    """
    - items boş olamaz
    - quantity > 0 olmalı
    - product_id tekrar edemez
    """
    items_list = list(items)
    if len(items_list) == 0:
        bad_request("items must not be empty")

    seen = set()
    for it in items_list:
        if it.quantity <= 0:
            bad_request("quantity must be > 0")
        if it.product_id in seen:
            bad_request("items contains duplicate product_id")
        seen.add(it.product_id)

    return items_list