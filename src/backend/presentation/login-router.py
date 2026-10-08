import os
from typing import Annotated

from fastapi import APIRouter, Body
from dotenvx import load_dotenvx

from backend.domain.Ports.repository import CheckLoginRepository
from backend.models.api_schemas.registration_and_login import LoginRequest

login_router = APIRouter()

load_dotenvx("config.env")
SECRET_KEY = os.getenv('SECRET_KEY')

def make_database() -> CheckLoginRepository:
  pass

@login_router.post("/account/login")
async def login_user(
  invalidated_user: Annotated[LoginRequest, Body()],
  user_database: Annotated[CheckLoginRepository, make_database()],
):
  found_user = user_database.check_if_user_exists(invalidated_user.email)