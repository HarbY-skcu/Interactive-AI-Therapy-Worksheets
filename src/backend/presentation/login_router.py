import os
from typing import Annotated

import bcrypt
import jwt
from fastapi import APIRouter, Body, HTTPException, status, Depends
from dotenvx import load_dotenvx

from backend.domain.Ports.encrypter import Encrypter
from backend.domain.Ports.repository import CheckLoginRepository
from backend.domain.service.authorization_service import TOKEN_TTL
from backend.infrastructure.encrypters.basic_encrypter import BasicJWTEncrypter
from backend.models.api_schemas.registration_and_login import LoginRequest

login_router = APIRouter()

load_dotenvx("config.env")
SECRET_KEY = os.getenv('SECRET_KEY')
PWD_ENCRYPTION_ALGORITHM = os.getenv('PWD_ENCRYPTION_ALGORITHM')

def make_database() -> CheckLoginRepository:
  pass

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

@login_router.post("/account/login")
async def login_user(
  invalidated_user: Annotated[LoginRequest, Body()],
  user_database: Annotated[CheckLoginRepository, Depends(make_database)],
  jwt_encrypter: Annotated[Encrypter, Depends(get_encrypter)]
):
  found_user = await user_database.fetch_user(invalidated_user.email)

  if not found_user or not bcrypt.checkpw(
    invalidated_user.password.get_secret_value().encode(),
    found_user.password.encode()
  ):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid Credentials",
    )

  token = jwt_encrypter.make_encrypted_token(
    found_user.user_id,
    found_user.user_type
  )

  return {
    "token": token,
    "user_id": found_user.user_id,
    "user_type": found_user.user_type,
  }