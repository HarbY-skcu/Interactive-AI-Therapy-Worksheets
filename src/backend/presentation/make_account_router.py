import os
from typing import Annotated, Generator, Dict, AsyncGenerator
import dotenvx
import asyncio
from contextlib import asynccontextmanager


from fastapi import APIRouter, Body, HTTPException, Depends, status, Request

from backend.domain.Ports.encrypter import Encrypter
from src.backend.domain.Ports.repository import CheckLoginRepository

from backend.infrastructure.encrypters.basic_encrypter import BasicJWTEncrypter
from backend.infrastructure.repository.async_postgres_db import AsyncPostgresDatabase
from backend.domain.service.authorization_service import TOKEN_TTL
from src.backend.models.api_schemas.registration_and_login import RegisterRequest, RegisterRequestResponse

@asynccontextmanager
async def item_lifespan(
  router: APIRouter,
) -> AsyncGenerator[Dict[str, AsyncPostgresDatabase], None]:
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

account_maker_router = APIRouter(lifespan = item_lifespan)
dotenvx.load_dotenv()

async def get_database(request: Request) -> CheckLoginRepository:
  return request.state.db

def get_encrypter() -> Encrypter:
  secret_key = os.getenv("SECRET_KEY")
  pwd_algorithm = os.getenv("PWD_ENCRYPTION_ALGORITHM")
  if not secret_key or not pwd_algorithm:
    raise ValueError("SECRET_KEY or PWD_ALGORITHM environment variable not set")

  return BasicJWTEncrypter(
    secret_key = secret_key,
    hashed_pwd_algorithm = pwd_algorithm,
    token_ttl = TOKEN_TTL
  )

@account_maker_router.post(
  "/account/register",
  response_model=RegisterRequestResponse,
  status_code=status.HTTP_201_CREATED,
)
async def create_account(
  proposed_user: Annotated[RegisterRequest, Body()],
  user_database: Annotated[CheckLoginRepository, Depends(get_database)],
  encryption: Annotated[Encrypter, Depends(get_encrypter)],
) -> RegisterRequestResponse:
  allowed_flag = await asyncio.create_task(
    user_database.check_if_credentials_are_allowed(
      password = proposed_user.password.get_secret_value(),
      email = proposed_user.email,
    )
  )
  if not allowed_flag:
    raise HTTPException(status_code=400, detail="Incorrect Credentials, try again")

  encrypted_data = encryption.encrypt(proposed_user.password.get_secret_value())

  await asyncio.create_task(
    user_database.create_new_user(
      email = proposed_user.email,
      password = encrypted_data.hashed_password.decode(),
      token = encrypted_data.token,
      user_type = proposed_user.user_type,
      user_id = encrypted_data.user_id
    )
  )

  return RegisterRequestResponse(
    token = encrypted_data.token,
    user_id = encrypted_data.user_id,
    user_type = proposed_user.user_type
  )