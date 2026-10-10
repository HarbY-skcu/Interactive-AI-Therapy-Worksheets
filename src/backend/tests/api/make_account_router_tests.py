import pytest

from fastapi.testclient import TestClient

from backend.tests.fixtures.make_account_router_fixtures import register_router, invalid_passwords, invalid_emails


def test_account_takes_valid_credentials(
  register_router: TestClient,
):
  response = register_router.post(
    '/account/register',
    headers={
      "email": "info@youremail.com",
      "password": "K#7v2bW9",
      "user_type": "Therapist"
    }
  )

  response_data = response.json()

  assert response.status_code == 201
  assert isinstance(response_data["token"], str) and response_data["token"]
  assert isinstance(response_data["user_id"], str) and response_data["user_id"]
  assert response_data["user_type"] == "Therapist"

@pytest.mark.parameterize(
  "password",
  invalid_passwords,
)
def test_signup_refuses_invalid_password(
  register_router: TestClient,
  password: str
):
  response = register_router.post(
    '/account/register',
    headers={
      "email": "info@youremail.com",
      "password": password,
      "user_type": "Therapist"
    }
  )

  assert response.status_code == 400
  assert response.json()["detail"] == "Incorrect Credentials, try again"
  assert password not in response.json()["detail"]

@pytest.mark.parameter(
  "email",
  invalid_emails,
)
def test_signup_refuses_invalid_email(
  register_router: TestClient,
  email: str
):
  response = register_router.post(
    '/account/register',
    headers={
      "email": email,
      "password": "K#7v2bW9",
      "user_type": "Therapist"
    }
  )

  assert response.status_code == 400
  assert response.json()["detail"] == "Invalid Email Address, try again"

@pytest.mark.parameter(
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
    headers={
      "email": "info@youremail.com",
      "password": "K#7v2bW9",
      "user_type": "Therapist"
    }
  )
  response = register_router.post(
    '/account/register',
    headers={
      "email": "info@youremail.com",
      "password": password,
      "user_type": "Client"
    }
  )

  assert response.status_code == 400
  assert response.json()["detail"] == "Invalid Operation: Account Already Exists"

def test_database_failure_during_request(
  register_router_without_db: TestClient
)