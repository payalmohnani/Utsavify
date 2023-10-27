import pytest
from app.main import app
from app import schemas
from jose import jwt
from app.config import settings


def test_create_user(client):
    res = client.post("/user", json={
        "first_name": "F_Name",
        "last_name": "L_Name",
        "email_id": "user@domain.com",
        "display_name": "disp",
        "password": "PASS",
        "college_roll_no": 102235
    }
    )
    assert res.status_code == 201


@pytest.mark.parametrize("email_id, password, status_code", {
    ("wrongmail@mail.com", "password123", 404),
    ("random@mail.com", "wrong_password", 404),
    (None, "password123", 422),
    ("random@mail.com", None, 422)
})
def test_incorrect_login(client, email_id, password, status_code):
    res = client.post(
        "/login", data={"username": email_id, "password": password})
    assert res.status_code == status_code


def test_get_user_by_id(client, test_user1, token):
    res = client.get(
        f'/user/{test_user1["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
