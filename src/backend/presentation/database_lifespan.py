import asyncio
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict

from fastapi import APIRouter, Request

from backend.domain.Ports.repository import CheckLoginRepository
from backend.infrastructure.repository.async_postgres_db import AsyncPostgresDatabase


@asynccontextmanager
async def item_lifespan(
  router: APIRouter,
) -> AsyncGenerator[Dict[str, AsyncPostgresDatabase], None]:
  """Open the database for the app's lifetime.

  Fails fast: if the database can't be reached the exception propagates and
  the application refuses to start.
  """
  db_url = os.getenv("DATABASE_URL")
  if not db_url:
    raise ValueError("DATABASE_URL environment variable not set")
  new_db = await asyncio.create_task(AsyncPostgresDatabase.create(
      db_url=db_url,
    )
  )
  try:
    yield {"db": new_db}
  finally:
    await new_db.close()


async def get_database(request: Request) -> CheckLoginRepository:
  return request.state.db
