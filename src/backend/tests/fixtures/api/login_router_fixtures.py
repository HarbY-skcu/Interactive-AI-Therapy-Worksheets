from pathlib import Path

import pytest
import uuid

from _pytest.monkeypatch import MonkeyPatch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import Generator

from backend.presentation.login_router import login_router
from backend.presentation.make_account_router import account_maker_router

@pytest.fixture(scope="session")
def login_router_fixture(
  monkeypatch: MonkeyPatch,
) -> TestClient:
  monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
  monkeypatch.setenv("SECRET_KEY", "test_secret_key")
  monkeypatch.setenv("PWD_ENCRYPTION_ALGORITHM", "HS256")
  test_app = FastAPI()
  test_app.include_router(login_router)
  test_app.include_router(account_maker_router)
  app = TestClient(test_app)
  app.post(
    '/account/register',
    headers={
      "email": "info@youremail.com",
      "password": "K#7v2bW9",
      "user_type": "Therapist"
    }
  )
  return app

@pytest.fixture
def login_router_without_db(
  monkeypatch: MonkeyPatch,
  tmp_path: Path,
) -> Generator[TestClient]:
  blocker_file = tmp_path / "not_a_dir.txt"
  blocker_file.write_text("I am a file, not a folder.")

  monkeypatch.setenv(
    "DATABASE_URL",
    f"sqlite+aiosqlite:////{blocker_file.resolve()}/db.sqlite"
  )
  monkeypatch.setenv("SECRET_KEY", "test_secret_key")
  monkeypatch.setenv("PWD_ENCRYPTION_ALGORITHM", "HS256")

  test_app = FastAPI()
  test_app.include_router(login_router)
  with TestClient(test_app) as client:
    yield client

invalid_password_and_emails =   [
  ("", ""),
  ("", "K#7v2bW9"),
  ("info@youremail.com", ""),
  ("info@youremail.com", "wrongpassw0rd*"),
  ("wrong@email.com", "K#7v2bW9"),
  ("wrong@email.com", "wrongpassw0rd*")
]

