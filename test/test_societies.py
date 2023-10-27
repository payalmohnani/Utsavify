import pytest
from app.main import app
from app import schemas
from jose import jwt
from app.config import settings


# Read society
def test_get_all_society(authorized_client, token, test_societies):
    res = authorized_client.get("/society/")
    # society_list = [schemas.SocietyOut(**id) for id in res.json()]

    assert (len(res.json())) == len(test_societies)
    assert res.status_code == 200


def test_get_society_by_id(client, test_user1, token, test_societies):
    res = client.get(f'/society/{test_societies[0].id}')
    assert res.status_code == 302

# get non-existing society


def test_get_society_by_id(client, test_user1, token, test_societies):
    res = client.get(f'/society/102212348')
    assert res.status_code == 404


# Creation
# create authorized society
def test_create_society(authorized_client, test_user1, test_societies):
    res = authorized_client.post("/society/",
                                 json={
                                     "name": "random_society",
                                     "college_level": True,
                                     "convenor": "Conv",
                                     "gen_sec": "Gen",
                                     "creator_id": test_user1["id"]
                                 })

    assert res.status_code == 201

# create existing society


def test_create_existing_society(authorized_client, test_user1, test_societies):
    res = authorized_client.post("/society/",
                                 json={
                                     "name": test_societies[0].name,
                                     "college_level": test_societies[0].college_level,
                                     "convenor": test_societies[0].convenor,
                                     "gen_sec": test_societies[0].gen_sec,
                                     "creator_id": test_user1["id"]
                                 })
    assert res.status_code == 409


# Updation
# Authorized updation
def test_update_society(authorized_client, test_user1, test_societies, token):

    res = authorized_client.put(f'/society/{test_societies[0].id}', headers={"Authorization": f"Bearer {token}"},
                                json={
                                    "name": test_societies[0].name,
                                    "college_level": test_societies[0].college_level,
                                    "convenor": "updated_conv",
                                    "gen_sec": "updated_gen_sec",
                                    "creator_id": test_user1["id"]
    })
    print(res.json())
    assert res.status_code == 202


# update society by changing name
def test_update_society_change_name(authorized_client, test_user1, test_societies, token):

    res = authorized_client.put(f'/society/{test_societies[0].id}', headers={"Authorization": f"Bearer {token}"},
                                json={
                                    "name": "update_name",
                                    "college_level": test_societies[0].college_level,
                                    "convenor": test_societies[0].convenor,
                                    "gen_sec": test_societies[0].gen_sec,
                                    "creator_id": test_user1["id"]
    })
    print(res.json())
    assert res.status_code == 409


# update non-existing society
def test_update_non_existing_society(authorized_client, test_user1, test_societies, token):

    res = authorized_client.put(f'/society/{78945646}', headers={"Authorization": f"Bearer {token}"},
                                json={
                                    "name": "update_name",
                                    "college_level": test_societies[0].college_level,
                                    "convenor": test_societies[0].convenor,
                                    "gen_sec": test_societies[0].gen_sec,
                                    "creator_id": test_user1["id"]
    })
    print(res.json())
    assert res.status_code == 404


# update unauthorized society
def test_update_unauthorized_society(authorized_client, test_user1, test_societies, token):

    res = authorized_client.put(f'/society/{test_societies[2].id}', headers={"Authorization": f"Bearer {token}"},
                                json={
                                    "name": test_societies[2].name,
                                    "college_level": test_societies[2].college_level,
                                    "convenor": test_societies[2].convenor,
                                    "gen_sec": test_societies[2].gen_sec,
                                    "creator_id": test_user1["id"]
    })
    print(res.json())
    assert res.status_code == 403


# Deletion
# authorized deletion
def test_delete_society(authorized_client, test_user1, test_societies, token):
    res = authorized_client.delete(
        f'/society/{test_societies[0].id}', headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 204


# unauthorized deletion
def test_delete_unauthorized_society(authorized_client, test_user1, test_societies, token):
    res = authorized_client.delete(
        f'/society/{test_societies[2].id}', headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 403

# non-existing society deletion


def test_delete_non_existing_society(authorized_client, test_user1, test_societies, token):
    res = authorized_client.delete(
        f'/society/1010123145', headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 404
