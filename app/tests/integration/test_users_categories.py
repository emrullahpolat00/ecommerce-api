def test_create_user_and_get(client):
    payload = {"email": "a@b.com", "full_name": "Alice"}
    r = client.post("/users", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["id"] > 0
    assert data["email"] == "a@b.com"
    assert data["full_name"] == "Alice"

    user_id = data["id"]
    r2 = client.get(f"/users/{user_id}")
    assert r2.status_code == 200
    assert r2.json()["email"] == "a@b.com"


def test_user_duplicate_email_returns_400(client):
    client.post("/users", json={"email": "dup@x.com", "full_name": "X"})
    r = client.post("/users", json={"email": "dup@x.com", "full_name": "Y"})
    assert r.status_code == 400
    assert "Email already exists" in r.text


def test_create_category_and_list(client):
    r = client.post("/categories", json={"name": "Electronics"})
    assert r.status_code == 201, r.text

    r2 = client.get("/categories")
    assert r2.status_code == 200
    names = [c["name"] for c in r2.json()]
    assert "Electronics" in names