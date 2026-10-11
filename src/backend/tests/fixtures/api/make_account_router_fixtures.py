from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import Generator

from backend.presentation.make_account_router import account_maker_router


@pytest.fixture(scope="session")
def register_router(
  monkeypatch: MonkeyPatch,
) -> TestClient:
  monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
  monkeypatch.setenv("SECRET_KEY", "test_secret_key")
  monkeypatch.setenv("PWD_ENCRYPTION_ALGORITHM", "HS256")
  test_app = FastAPI()
  test_app.include_router(account_maker_router)
  return TestClient(test_app)

@pytest.fixture
def register_router_without_db(
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
  test_app.include_router(account_maker_router)

  with TestClient(test_app) as client:
    yield client


invalid_passwords = [
  "2Happy!",
  "67676767",
  "ReallyReallyReallyReallyReally"
  "ReallyReallyReallyReallyReally"
  "ReallyReallyReallyReally"
  "LongPassword100!",
  "#$%*@#@*&#@*)*%",
  r"\F\o\n\a\r\t" + '\\',
  "",
  "xdx"
  "1234%^&*"
]

invalid_emails = [
  "user@",
  "@invalid.com",
  ".me@example.com",
  "me@example..com",
  "me.example@com",
  r"me\@example.com"
]