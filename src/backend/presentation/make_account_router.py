import os
from typing import Annotated
import dotenvx
import asyncio


from fastapi import APIRouter, Body, HTTPException, Depends, status

from backend.domain.Ports.encrypter import Encrypter
from backend.domain.Ports.repository import CheckLoginRepository

from backend.infrastructure.encrypters.basic_encrypter import BasicJWTEncrypter
from backend.domain.service.authorization_service import TOKEN_TTL
from backend.models.api_schemas.registration_and_login import RegisterRequest, RegisterResponse
from backend.presentation.database_lifespan import get_database, item_lifespan

account_maker_router = APIRouter(lifespan = item_lifespan)
dotenvx.load_dotenv("src/backend/config.env")

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
  response_model=RegisterResponse,
  status_code=status.HTTP_201_CREATED,
)
async def create_account(
  proposed_user: Annotated[RegisterRequest, Body()],
  user_database: Annotated[CheckLoginRepository, Depends(get_database)],
  jwt_encrypter: Annotated[Encrypter, Depends(get_encrypter)],
) -> RegisterResponse:
  allowed_flag = await asyncio.create_task(
    user_database.check_if_credentials_are_allowed(
      email = proposed_user.email,
    )
  )
  if not allowed_flag:
    raise HTTPException(status_code=400, detail="Account is already registered")

  encrypted_data = jwt_encrypter.encrypt_password(
    proposed_user.password.get_secret_value()
  )

  await asyncio.create_task(
    user_database.create_new_user(
      email = proposed_user.email,
      password = encrypted_data.hashed_password.decode("utf-8"),
      user_type = proposed_user.user_type,
      user_id = encrypted_data.user_id
    )
  )

  return RegisterResponse(
    user_id = encrypted_data.user_id,
    user_type = proposed_user.user_type
  )