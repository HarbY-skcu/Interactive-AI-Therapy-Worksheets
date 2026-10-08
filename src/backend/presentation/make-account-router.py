import os
from typing import Annotated
import dotenvx
import asyncio
import logging

from fastapi import APIRouter, Body, HTTPException

from backend.domain.Ports.email_service import EmailService
from backend.domain.Ports.encrypter import Encrypter
from src.backend.models.api_schemas.registration_and_login import RegisterRequest, LoginRequest
from src.backend.domain.Ports.repository import CheckLoginRepository

account_maker_router = APIRouter()
dotenvx.load_dotenv()

def make_database() -> CheckLoginRepository:
  pass

def make_email_service() -> EmailService:
  pass

def make_encrypter() -> Encrypter:
  pass

@account_maker_router.post("/account/register")
async def create_account(
  proposed_user: Annotated[RegisterRequest, Body()],
  user_database: Annotated[CheckLoginRepository, make_database()],
  email_service: Annotated[EmailService, make_email_service()],
  encryption: Annotated[Encrypter, make_encrypter()],
):
  if not user_database.check_if_credentials_are_allowed(
    password = proposed_user.password,
    email = proposed_user.email,
  ):
    raise HTTPException(status_code=400, detail="Incorrect Credentials, try again")

  # hashed_password = bcrypt.hashpw(proposed_user.password.encode(), bcrypt.gensalt())
  # user_id = str(uuid.uuid4())
  # token = jwt.encode(
  #   {"user_id": user_id},
  #   os.getenv("SECRET_KEY"),
  #   algorithm= os.getenv("PWD_ENCRYPTION_ALGORITHM")
  # )
  #
  # !!! Put into class that realizes Encrypter !!!

  encrypted_data = encryption.encrypt(proposed_user.password)

  verify_email_task = asyncio.create_task(email_service.verify_email(proposed_user.email))
  try:
    await verify_email_task
  except asyncio.TimeoutError:
    raise HTTPException(
      status_code=400,
      detail=f"Email Unverified After 10 Minute Window:"
             f" {proposed_user.email}"
    )

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

  return {
    "token": encrypted_data.token,
    "user_id": encrypted_data.user_id,
    "user_type": proposed_user.user_type
  }