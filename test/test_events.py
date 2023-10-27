import pytest
from app.main import app
from app import schemas
from fastapi.testclient import TestClient
from jose import jwt
from app.config import settings
import json
from datetime import datetime


# Read society
def test_get_all_events(authorized_client, token, test_societies, test_events):
    res = authorized_client.get("/event/")

    assert(len(res.json())) == len(test_events)
    assert res.status_code == 200


# get event by id
def test_get_event_by_id(client, test_user1, token, test_societies, test_events):
    res = client.get(f'/event/{test_events[0].id}')
    assert res.status_code == 302

# get non-existing event
def test_get_event_by_id(client, test_user1, token, test_societies, test_events):
    res = client.get(f'/event/1024623115')
    assert res.status_code == 404


# Creation
# create authorized society
def test_create_event(authorized_client, test_user1, test_societies, test_events):
    res = authorized_client.post("/event/", json={
                                                "name": "Event",
                                                "organizing_society": test_societies[0].name,
                                                "event_time": "2023-10-22T10:59:45.245Z",
                                                })
    assert res.status_code == 201

# create event by non-existing-society
def test_create_existing_society(authorized_client, test_user1, test_societies, test_events):
    res = authorized_client.post("/event/", json={
                                                    "name": "Event",
                                                    "organizing_society": "society_nameqwertyuiodfghjk",
                                                    "event_time": "2023-10-22T10:59:45.245Z",
                                                    })
    assert res.status_code == 409
 

# create existing event 
def test_create_existing_event(authorized_client, token, test_user1, test_societies, test_events):
    res = authorized_client.post("/event/", json={
                                                    "name": test_events[0].name,
                                                    "organizing_society":test_events[0].organizing_society,
                                                    "event_time": f'{test_events[0].event_time}'
                                                    })
    assert res.status_code == 409
 


# Updation
# Authorized updation
def test_update_society(authorized_client, test_user1, test_societies, test_events, token):

    res = authorized_client.put(f'/event/{test_events[0].id}',headers={"Authorization": f"Bearer {token}"},
                                json={"name": "new_name",
                                      "organizing_society":test_events[0].organizing_society,
                                      "event_time": str(test_events[0].event_time)}
                                      )
    assert res.status_code == 202


# update non-existing society 
def test_update_non_existing_society(authorized_client, test_user1, test_societies, token, test_events):

    res = authorized_client.put(f'/event/78924312',headers={"Authorization": f"Bearer {token}"},
                                json={"name": "new_name",
                                      "organizing_society":test_events[0].organizing_society,
                                      "event_time": str(test_events[0].event_time)}
                                      )
    assert res.status_code == 404


# update unauthorized society 
def test_update_unauthorized_society(authorized_client, test_user1, test_societies, token, test_events):

    res = authorized_client.put(f'/event/{test_events[2].id}',headers={"Authorization": f"Bearer {token}"},
                                json={
                                    "name": "new_name",
                                    "organizing_society" : test_events[2].organizing_society,
                                    "event_time": str(test_events[2].event_time)
                                    })
    assert res.status_code == 403


# Deletion
# authorized deletion
def test_delete_event(authorized_client, test_user1, test_societies, token, test_events):
    res = authorized_client.delete(f'/event/{test_events[0].id}',headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 204


# unauthorized deletion
def test_delete_unauthorized_event(authorized_client, test_user1, test_societies, token, test_events):
    
    res = authorized_client.delete(f'/event/{test_events[2].id}',headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403


# non-existing event deletion
def test_delete_non_existing_event(authorized_client, test_user1, test_societies, token, test_events):
 
    res = authorized_client.delete(f'/event/1010123145',headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404

