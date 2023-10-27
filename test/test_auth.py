from app.config import settings
from app import schemas
from jose import jwt


def test_login_user(client, test_user1):
    res = client.post(
        "/login", data={"username": test_user1["email_id"], "password": test_user1["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload["current_user"]
    assert id == test_user1["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
