import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
from app.database import get_db
from app.main import app
from app import models
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/test_{settings.DATABASE_NAME}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):

    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user1(client):
    user_data = {
        "first_name": "FName",
        "last_name": "LName",
        "email_id": "username@domain.com",
                    "display_name": "disp",
                    "password": "PASS",
                    "college_roll_no": 1,

    }

    res = client.post("/user", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {
        "first_name": "User2Name",
        "last_name": "User2LName",
        "email_id": "user2name@domain.com",
                    "display_name": "disp2",
                    "password": "PASS",
                    "college_roll_no": 2
    }

    res = client.post("/user", json=user_data)
    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user1):
    return create_access_token({"current_user": test_user1["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_events(test_user1, test_user2, session):
    test_event_data = [
        {
            "name": "event1",
            "organizing_society": "test_society_1",
            "event_time": "2023-10-21T16:22:58.322Z",
            "creator_id": test_user1["id"]
        },
        {
            "name": "event2",
            "organizing_society": "test_society_2",
            "event_time": "2023-11-21T16:22:18.322Z",
            "creator_id": test_user1["id"]
        },
        {
            "name": "event3",
            "organizing_society": "test_society_1",
            "event_time": "2023-10-25T16:22:08.322Z",
            "creator_id": test_user2["id"]
        }
    ]

    all_events = [models.Event(**test_event) for test_event in test_event_data]

    session.add_all(all_events)

    session.commit()
    session.query(models.Event).all()
    return all_events


@pytest.fixture
def test_societies(authorized_client, test_user1, test_user2, session):
    test_society_data = [
        {
            "name": "test_society_1",
            "college_level": True,
            "convenor": "Conv",
            "gen_sec": "Gen",
            "creator_id": test_user1["id"]
        },
        {
            "name": "test_society_2",
            "college_level": True,
            "convenor": "Conv",
            "gen_sec": "Gen",
            "creator_id": test_user1["id"]
        },
        {
            "name": "test_society_3",
            "college_level": True,
            "convenor": "Conv",
            "gen_sec": "Gen",
            "creator_id": test_user2["id"]
        }
    ]

    all_societies = [models.Society(**test_society)
                     for test_society in test_society_data]

    session.add_all(all_societies)

    session.commit()
    session.query(models.Society).all()
    return all_societies
