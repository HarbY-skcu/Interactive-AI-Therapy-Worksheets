import pytest
from fastapi.testclient import TestClient
from typing import Generator

from backend.tests.fixtures.login_router_fixtures import login_router_fixture


def test_database_failure_during_request(
  login_router_without_db: Generator[TestClient]
):
  router = next(login_router_without_db)
  response = router.post(
    '/account/login',
    headers={
      "email": "info@youremail.com",
      "password": "K#7v2bW9",
      "user_type": "Therapist"
    }
  )

  assert response.status_code == 500
  assert response.json()["detail"] == "Database Not Operational"

def test_login_with_new_user(
  login_router_fixture: TestClient,
):
  response = login_router_fixture.post(
    '/account/login',
    headers={
      "email": "info@youremail.com",
      "password": "K#7v2bW9",
    }
  )
  response_data = response.json()

  assert response.status_code == 200
  assert response_data["detail"] == "Successful Login"
  assert isinstance(response_data["token"], str) and response_data["token"]
  assert isinstance(response_data["user_id"], str) and response_data["user_id"]
  assert response_data["user_type"] == "Therapist"

@pytest.mark.parameterize(
  "email,password",
  [
    ("", ""),
    ("", "K#7v2bW9"),
    ("info@youremail.com", ""),
    ("info@youremail.com", "wrongpassw0rd*"),
    ("wrong@email.com", "K#7v2bW9"),
    ("wrong@email.com", "wrongpassw0rd*")
  ]
)
def test_login_with_wrong_credentials(
  login_router_fixture: TestClient,
  email: str,
  password: str,
):
  response = login_router_fixture.post(
    "/account/login",
    headers={
      "email": email,
      "password": password
    }
  )

  assert response.status_code == 400
  assert response.json()["detail"] == "Wrong Email or Password"