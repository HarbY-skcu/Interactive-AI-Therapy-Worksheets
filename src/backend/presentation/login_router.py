import os
from typing import Annotated

import bcrypt
import jwt
from fastapi import APIRouter, Body, HTTPException, status, Depends
from dotenvx import load_dotenvx

from backend.domain.Ports.repository import CheckLoginRepository
from backend.models.api_schemas.registration_and_login import LoginRequest

login_router = APIRouter()

load_dotenvx("config.env")
SECRET_KEY = os.getenv('SECRET_KEY')
PWD_ENCRYPTION_ALGORITHM = os.getenv('PWD_ENCRYPTION_ALGORITHM')

def make_database() -> CheckLoginRepository:
  pass

@login_router.post("/account/login")
async def login_user(
  invalidated_user: Annotated[LoginRequest, Body()],
  user_database: Annotated[CheckLoginRepository, Depends(make_database)],
):
  found_user = await user_database.fetch_user(invalidated_user.email)
  if not found_user or not bcrypt.checkpw(
    invalidated_user.password.encode(),
    found_user.password.encode()
  ):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid Credentials",
    )

  token = jwt.encode(
    {"user_id": found_user.user_id},
    SECRET_KEY,
    algorithm=PWD_ENCRYPTION_ALGORITHM
  )

  return {
    "token": token,
    "user_id": found_user.user_id,
    "user_type": found_user.user_type,
  }