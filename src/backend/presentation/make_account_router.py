import os
from typing import Annotated
import dotenvx
import asyncio


from fastapi import APIRouter, Body, HTTPException, Depends, status
from pydantic import SecretStr

from backend.domain.Ports.encrypter import Encrypter
from src.backend.models.api_schemas.registration_and_login import RegisterRequest, RegisterRequestResponse
from src.backend.domain.Ports.repository import CheckLoginRepository

account_maker_router = APIRouter()
dotenvx.load_dotenv()

def make_database() -> CheckLoginRepository:
  pass

def make_encrypter() -> Encrypter:
  pass

@account_maker_router.post(
  "/account/register",
  response_model=RegisterRequestResponse,
  status_code=status.HTTP_201_CREATED,
)
async def create_account(
  proposed_user: Annotated[RegisterRequest, Body()],
  user_database: Annotated[CheckLoginRepository, Depends(make_database)],
  encryption: Annotated[Encrypter, Depends(make_encrypter)],
) -> RegisterRequestResponse:
  allowed_flag = await user_database.check_if_credentials_are_allowed(
    password = proposed_user.password.get_secret_value(),
    email = proposed_user.email,
  )
  if not allowed_flag:
    raise HTTPException(status_code=400, detail="Incorrect Credentials, try again")

  encrypted_data = encryption.encrypt(proposed_user.password.get_secret_value())

  login_task = asyncio.create_task(
    user_database.create_new_user(
      email = proposed_user.email,
      password = encrypted_data.hashed_password.decode(),
      token = encrypted_data.token,
      user_type = proposed_user.user_type,
      user_id = encrypted_data.user_id
    )
  )
  await login_task

  return RegisterRequestResponse(
    token = encrypted_data.token,
    user_id = encrypted_data.user_id,
    user_type = proposed_user.user_type
  )