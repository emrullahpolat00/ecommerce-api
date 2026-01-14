def create_user(client, email="e2e@x.com", name="E2E User"):
    r = client.post("/users", json={"email": email, "full_name": name})
    assert r.status_code == 201, r.text
    return r.json()["id"]


def create_category(client, name="E2E Category"):
    r = client.post("/categories", json={"name": name})
    assert r.status_code == 201, r.text
    return r.json()["id"]


def create_product(client, category_id, name="E2E Product", price=10.0):
    r = client.post("/products", json={"name": name, "price": price, "category_id": category_id})
    assert r.status_code == 201, r.text
    return r.json()["id"]


def create_order(client, user_id, items):
    r = client.post("/orders", json={"user_id": user_id, "items": items})
    assert r.status_code == 201, r.text
    return r.json()


def create_review(client, user_id, product_id, rating=5, comment="ok"):
    r = client.post("/reviews", json={
        "user_id": user_id, "product_id": product_id, "rating": rating, "comment": comment
    })
    assert r.status_code == 201, r.text
    return r.json()


def test_e2e_flow_1_category_product_order_get(client):
    user_id = create_user(client, "flow1@x.com")
    cat_id = create_category(client, "Flow1 Category")
    p1 = create_product(client, cat_id, "Flow1 P1", 20.0)
    p2 = create_product(client, cat_id, "Flow1 P2", 30.0)

    order = create_order(client, user_id, [
        {"product_id": p1, "quantity": 2},
        {"product_id": p2, "quantity": 1},
    ])

    r = client.get(f"/orders/{order['id']}")
    assert r.status_code == 200
    data = r.json()
    assert data["user_id"] == user_id
    assert len(data["items"]) == 2


def test_e2e_flow_2_review_create_update_delete(client):
    user_id = create_user(client, "flow2@x.com")
    cat_id = create_category(client, "Flow2 Category")
    p1 = create_product(client, cat_id, "Flow2 P1", 50.0)

    review = create_review(client, user_id, p1, rating=4, comment="nice")
    rid = review["id"]

    r2 = client.put(f"/reviews/{rid}", json={"rating": 5, "comment": "updated"})
    assert r2.status_code == 200
    assert r2.json()["rating"] == 5

    r3 = client.delete(f"/reviews/{rid}")
    assert r3.status_code == 204

    r4 = client.get(f"/reviews/{rid}")
    assert r4.status_code == 404


def test_e2e_flow_3_delete_category_cascades_products(client):
    cat_id = create_category(client, "Flow3 Category")
    p1 = create_product(client, cat_id, "Flow3 P1", 10.0)

    # category sil
    r = client.delete(f"/categories/{cat_id}")
    assert r.status_code == 204

    # ürün de cascade ile silinmiş olmalı
    r2 = client.get(f"/products/{p1}")
    assert r2.status_code == 404


def test_e2e_flow_4_invalid_requests_return_expected_codes(client):
    # olmayan user
    r = client.get("/users/99999")
    assert r.status_code == 404

    # boş category name
    r2 = client.post("/categories", json={"name": "   "})
    assert r2.status_code == 400

    # invalid product category
    r3 = client.post("/products", json={"name": "X", "price": 10.0, "category_id": 99999})
    assert r3.status_code == 400


def test_e2e_flow_5_lists_work(client):
    create_user(client, "flow5@x.com")
    create_category(client, "Flow5 Category")

    r1 = client.get("/users")
    r2 = client.get("/categories")
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert len(r1.json()) >= 1
    assert len(r2.json()) >= 1