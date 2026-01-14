import pytest
from fastapi import HTTPException

from app.services.validation import (
    normalize_name,
    validate_non_empty,
    validate_price,
    validate_rating,
    validate_order_items,
    OrderItemIn,
)


def test_normalize_name_trims_and_collapses_spaces():
    assert normalize_name("  Hello   World  ") == "Hello World"


def test_validate_non_empty_ok():
    assert validate_non_empty("  x  ", "name") == "x"


def test_validate_non_empty_raises():
    with pytest.raises(HTTPException) as e:
        validate_non_empty("   ", "name")
    assert e.value.status_code == 400


def test_validate_price_ok():
    assert validate_price(10.5) == 10.5


def test_validate_price_raises_on_zero():
    with pytest.raises(HTTPException) as e:
        validate_price(0)
    assert e.value.status_code == 400


def test_validate_price_raises_on_negative():
    with pytest.raises(HTTPException) as e:
        validate_price(-1)
    assert e.value.status_code == 400


def test_validate_rating_ok_low_high():
    assert validate_rating(1) == 1
    assert validate_rating(5) == 5


def test_validate_rating_raises_low():
    with pytest.raises(HTTPException) as e:
        validate_rating(0)
    assert e.value.status_code == 400


def test_validate_rating_raises_high():
    with pytest.raises(HTTPException) as e:
        validate_rating(6)
    assert e.value.status_code == 400


def test_validate_order_items_ok():
    items = validate_order_items([
        OrderItemIn(product_id=1, quantity=2),
        OrderItemIn(product_id=2, quantity=1),
    ])
    assert len(items) == 2


def test_validate_order_items_empty_raises():
    with pytest.raises(HTTPException) as e:
        validate_order_items([])
    assert e.value.status_code == 400
    assert "items must not be empty" in str(e.value.detail)


def test_validate_order_items_duplicate_product_raises():
    with pytest.raises(HTTPException) as e:
        validate_order_items([
            OrderItemIn(product_id=1, quantity=1),
            OrderItemIn(product_id=1, quantity=2),
        ])
    assert e.value.status_code == 400
    assert "duplicate" in str(e.value.detail)


def test_validate_order_items_quantity_zero_raises():
    with pytest.raises(HTTPException) as e:
        validate_order_items([OrderItemIn(product_id=1, quantity=0)])
    assert e.value.status_code == 400