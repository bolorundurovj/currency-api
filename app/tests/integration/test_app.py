import os
import random
import string
from fastapi.testclient import TestClient
from web import app

client = TestClient(app)


TEST_MAIL = "{}@gmail.test".format('test'.join((random.choice(string.ascii_lowercase) for x in range(4))))
TOKEN = None


def test_app_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API up and running"}


def test_retrieve_currencies_forbidden():
    response = client.get("/currencies")
    assert response.status_code == 403


def test_retrieve_currencies_unauthorized():
    response = client.get(
        "/currencies",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjU2ODQ5NjQxLCJpYXQiOjE2NTY4NDc4NDEsInN1YiI6eyJpZCI6OCwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImZ1bGxfbmFtZSI6IlRlc3QgRG9lIn19.VLzpnJRnMM1pYjTO1ui7qYGUDPEDWZ1EkWPzVdnv5mA"
        },
    )
    assert response.status_code == 401


def test_convert_currency_forbidden():
    response = client.post(
        "/currencies/convert",
        json={"from_currency": "USD", "to_currency": "GBP", "amount": 0},
    )
    assert response.status_code == 403


def test_convert_currency_unauthorized():
    response = client.post(
        "/currencies/convert",
        json={"from_currency": "USD", "to_currency": "GBP", "amount": 0},
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjU2ODQ5NjQxLCJpYXQiOjE2NTY4NDc4NDEsInN1YiI6eyJpZCI6OCwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImZ1bGxfbmFtZSI6IlRlc3QgRG9lIn19.VLzpnJRnMM1pYjTO1ui7qYGUDPEDWZ1EkWPzVdnv5mA"
        },
    )
    assert response.status_code == 401


def test_incorrect_register():
    response = client.post(
        "/auth/signup",
        json={"email": "testyahoo.com", "password": "12345"},
    )
    assert response.status_code == 400


def test_incorrect_login():
    response = client.post(
        "/auth/login",
        json={"email": "currency_test@yahoo.com", "password": "1234"},
    )
    assert response.status_code == 400


def test_correct_register():
    response = client.post(
        "/auth/signup",
        json={"email": TEST_MAIL, "password": "12345"},
    )
    assert response.status_code == 201


def test_correct_login():
    response = client.post(
        "/auth/login",
        json={"email": TEST_MAIL, "password": "12345"},
    )
    assert response.status_code == 200
    global TOKEN
    TOKEN = response.json().get("data").get("access_token")


def test_retrieve_currencies_success():
    response = client.get(
        "/currencies",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json().get("status", False) == True
    assert type(response.json().get("data", None)) == list


