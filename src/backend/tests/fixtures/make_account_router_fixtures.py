import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import create_engine
fr
from backend.presentation.make_account_router import account_maker_router


@pytest.fixture(scope="session")
def register_router(
) -> TestClient:
  test_app = FastAPI()
  test_app.include_router(account_maker_router)
  return TestClient(test_app)

bad_engine = create_engine("sqlite:////nonexistent_dir/db.sqlite")
BadSession = sessionmaker(bind=bad_engine)

@pytest.fixture
def register_router_without_db(
) -> TestClient:
  test_app = FastAPI()
  test_app.include_router(account_maker_router)
  test_app.dependency_overrides["user_database"] =
  return TestClient(test_app)


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

print(r"\F\o\n\a\r\t" + "\\")

invalid_emails = [
  "user@",
  "@invalid.com",
  ".me@example.com",
  "me@example..com",
  "me.example@com",
  r"me\@example.com"
]