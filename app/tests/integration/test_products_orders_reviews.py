def _create_user(client, email="u@x.com"):
    r = client.post("/users", json={"email": email, "full_name": "User"})
    assert r.status_code == 201, r.text
    return r.json()["id"]


def _create_category(client, name="Cat 1"):
    r = client.post("/categories", json={"name": name})
    assert r.status_code == 201, r.text
    return r.json()["id"]


def _create_product(client, category_id, name="P1", price=10.0):
    r = client.post("/products", json={"name": name, "price": price, "category_id": category_id})
    assert r.status_code == 201, r.text
    return r.json()["id"]


def test_create_product_with_invalid_category_returns_400(client):
    r = client.post("/products", json={"name": "P", "price": 10.0, "category_id": 9999})
    assert r.status_code == 400


def test_create_product_with_blank_name_returns_400(client):
    cat_id = _create_category(client)
    r = client.post("/products", json={"name": "   ", "price": 10.0, "category_id": cat_id})
    assert r.status_code == 400


def test_create_product_with_negative_price_returns_422_or_400(client):
    # Pydantic Field(gt=0) 422 döndürebilir, service validate_price da 400 döndürebilir.
    cat_id = _create_category(client)
    r = client.post("/products", json={"name": "P", "price": -5.0, "category_id": cat_id})
    assert r.status_code in (400, 422)


def test_order_create_empty_items_returns_422_or_400(client):
    user_id = _create_user(client, "o1@x.com")
    r = client.post("/orders", json={"user_id": user_id, "items": []})
    assert r.status_code in (400, 422)


def test_order_create_duplicate_product_returns_400(client):
    user_id = _create_user(client, "o2@x.com")
    cat_id = _create_category(client, "Electronics")
    p1 = _create_product(client, cat_id, "Phone", 100.0)

    r = client.post("/orders", json={
        "user_id": user_id,
        "items": [{"product_id": p1, "quantity": 1}, {"product_id": p1, "quantity": 2}]
    })
    assert r.status_code == 400


def test_order_create_success_and_get(client):
    user_id = _create_user(client, "o3@x.com")
    cat_id = _create_category(client, "Food")
    p1 = _create_product(client, cat_id, "Apple", 3.0)
    p2 = _create_product(client, cat_id, "Bread", 5.0)

    r = client.post("/orders", json={
        "user_id": user_id,
        "items": [{"product_id": p1, "quantity": 2}, {"product_id": p2, "quantity": 1}]
    })
    assert r.status_code == 201, r.text
    order = r.json()
    assert len(order["items"]) == 2

    r2 = client.get(f"/orders/{order['id']}")
    assert r2.status_code == 200
    assert len(r2.json()["items"]) == 2


def test_review_duplicate_user_product_returns_400(client):
    user_id = _create_user(client, "r1@x.com")
    cat_id = _create_category(client, "Books")
    prod_id = _create_product(client, cat_id, "Book", 20.0)

    r1 = client.post("/reviews", json={"user_id": user_id, "product_id": prod_id, "rating": 5, "comment": "ok"})
    assert r1.status_code == 201, r1.text

    r2 = client.post("/reviews", json={"user_id": user_id, "product_id": prod_id, "rating": 4, "comment": "again"})
    assert r2.status_code == 400


def test_review_update_rating_out_of_range_returns_422_or_400(client):
    user_id = _create_user(client, "r2@x.com")
    cat_id = _create_category(client, "Games")
    prod_id = _create_product(client, cat_id, "Game", 60.0)

    r = client.post("/reviews", json={"user_id": user_id, "product_id": prod_id, "rating": 5})
    assert r.status_code == 201, r.text
    review_id = r.json()["id"]

    r2 = client.put(f"/reviews/{review_id}", json={"rating": 10})
    assert r2.status_code in (400, 422)