import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from backend.tests.fixtures.api.make_account_router_fixtures import invalid_passwords, invalid_emails


def test_account_takes_valid_credentials(
  register_router: TestClient,
):
  response = register_router.post(
    '/account/register',
    json={
      "email": "info@youremail.com",
      "password": "K#7v2bW9",
      "user_type": "Therapist"
    }
  )

  response_data = response.json()

  assert response.status_code == 201
  assert isinstance(response_data["user_id"], str) and response_data["user_id"]
  assert response_data["user_type"] == "therapist"

@pytest.mark.parametrize(
  "password",
  invalid_passwords,
)
def test_signup_refuses_invalid_password(
  register_router: TestClient,
  password: str
):
  response = register_router.post(
    '/account/register',
    json={
      "email": "info@youremail.com",
      "password": password,
      "user_type": "Therapist"
    }
  )

  assert response.status_code == 400
  assert response.json()["detail"] == "Incorrect Credentials, try again"
  assert not password or password not in response.json()["detail"]

@pytest.mark.parametrize(
  "email",
  invalid_emails,
)
def test_signup_refuses_invalid_email(
  register_router: TestClient,
  email: str
):
  response = register_router.post(
    '/account/register',
    json={
      "email": email,
      "password": "K#7v2bW9",
      "user_type": "Therapist"
    }
  )

  assert response.status_code == 400
  assert response.json()["detail"] == "Invalid Email Address, Try Again"

@pytest.mark.parametrize(
  "password",
  [
    "K#7v2bW9",
    "9Wb2v7#k"
  ]
)
def test_restriction_of_making_multiple_accounts_on_the_same_email(
  register_router: TestClient,
  password: str
):
  register_router.post(
    '/account/register',
    json={
      "email": "info@youremail.com",
      "password": "K#7v2bW9",
      "user_type": "Therapist"
    }
  )
  response = register_router.post(
    '/account/register',
    json={
      "email": "info@youremail.com",
      "password": password,
      "user_type": "Client"
    }
  )

  assert response.status_code == 400
  assert response.json()["detail"] == "Account is already registered"

def test_app_refuses_to_start_without_database(
  register_app_without_db: FastAPI
):
  with pytest.raises(OperationalError):
    with TestClient(register_app_without_db):
      pass
