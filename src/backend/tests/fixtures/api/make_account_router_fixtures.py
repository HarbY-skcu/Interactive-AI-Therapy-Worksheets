import os
from pathlib import Path

import pytest
import pytest_asyncio
from _pytest.monkeypatch import MonkeyPatch
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import Generator

from sqlalchemy import text, NullPool
from sqlalchemy.ext.asyncio import create_async_engine
from testcontainers.community.postgres import PostgresContainer

from backend.models.data_models import Base
from backend.presentation import account_maker_router, register_validation_handlers


@pytest.fixture(scope="function")
def register_router(
  clean_db: None,
  postgres_url: str,
  monkeypatch: MonkeyPatch,
) -> Generator[TestClient]:
  monkeypatch.setenv("DATABASE_URL", postgres_url)
  monkeypatch.setenv("SECRET_KEY", "test_secret_key")
  monkeypatch.setenv("PWD_ENCRYPTION_ALGORITHM", "HS256")
  test_app = FastAPI()
  register_validation_handlers(test_app)
  test_app.include_router(account_maker_router)
  with TestClient(test_app) as client:
    yield client

@pytest.fixture(scope="session")
def postgres_url() -> Generator[str]:
  with PostgresContainer("postgres:16", driver="asyncpg") as postgres:
    db_url = postgres.get_connection_url()

    backend_dir = Path(__file__).parents[3]
    alembic_cfg = Config(str(backend_dir / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(backend_dir / "alembic"))

    # alembic/env.py is synchronous and reads DATABASE_URL from the environment
    previous = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = db_url.replace("+asyncpg", "+psycopg")
    try:
      command.upgrade(alembic_cfg, "head")
    finally:
      if previous is None:
        os.environ.pop("DATABASE_URL", None)
      else:
        os.environ["DATABASE_URL"] = previous

    yield db_url

@pytest_asyncio.fixture(scope="function")
async def clean_db(
  postgres_url: str,
):
  yield

  table_names = ", ".join(t.name for t in Base.metadata.sorted_tables)
  if table_names:
    engine = create_async_engine(postgres_url, poolclass=NullPool)
    async with engine.begin() as conn:
      await conn.execute(
        text(f"TRUNCATE TABLE {table_names} RESTART IDENTITY CASCADE;")
      )
    await engine.dispose()

@pytest.fixture
def register_app_without_db(
  monkeypatch: MonkeyPatch,
  tmp_path: Path,
) -> FastAPI:
  blocker_file = tmp_path / "not_a_dir.txt"
  blocker_file.write_text("I am a file, not a folder.")

  monkeypatch.setenv(
    "DATABASE_URL",
    f"sqlite+aiosqlite:////{blocker_file.resolve()}/db.sqlite"
  )
  monkeypatch.setenv("SECRET_KEY", "test_secret_key")
  monkeypatch.setenv("PWD_ENCRYPTION_ALGORITHM", "HS256")

  test_app = FastAPI()
  register_validation_handlers(test_app)
  test_app.include_router(account_maker_router)

  return test_app


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