import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError


def test_app_refuses_to_start_without_database(
  login_app_without_db: FastAPI
):
  with pytest.raises(OperationalError):
    with TestClient(login_app_without_db):
      pass

def test_login_with_new_user(
  login_router_fixture: TestClient,
):
  response = login_router_fixture.post(
    '/account/login',
    json={
      "email": "info@youremail.com",
      "password": "K#7v2bW9",
    }
  )
  response_data = response.json()

  assert response.status_code == 200
  assert isinstance(response_data["token"], str) and response_data["token"]
  assert isinstance(response_data["user_id"], str) and response_data["user_id"]
  assert response_data["user_type"] == "therapist"

@pytest.mark.parametrize(
  "email,password",
  [
    ("", ""),
    ("", "K#7v2bW9"),
    ("info@youremail.com", ""),
    ("info@youremail.com", "wrongpassw0rd*"),
  ]
)
def test_login_with_malformed_credentials(
  login_router_fixture: TestClient,
  email: str,
  password: str,
):
  response = login_router_fixture.post(
    "/account/login",
    json={
      "email": email,
      "password": password
    }
  )

  assert response.status_code == 400
  assert response.json()["detail"] in (
    "Invalid Email Address, Try Again",
    "Incorrect Credentials, try again",
  )
  assert not password or password not in response.json()["detail"]

@pytest.mark.parametrize(
  "email,password",
  [
    ("wrong@email.com", "K#7v2bW9"),
    ("wrong@email.com", "Wr0ngpassw*rd"),
    ("info@youremail.com", "Wr0ngpassw*rd"),
  ]
)
def test_login_with_wrong_credentials(
  login_router_fixture: TestClient,
  email: str,
  password: str,
):
  response = login_router_fixture.post(
    "/account/login",
    json={
      "email": email,
      "password": password
    }
  )

  assert response.status_code == 401
  assert response.json()["detail"] == "Invalid Credentials"
