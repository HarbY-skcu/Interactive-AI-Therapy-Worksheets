import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from backend.domain.Ports.user_authorization import GetCurrentUser, RequireRole

import jwt
from dotenvx import load_dotenvx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenvx("config.env")
SECRET_KEY = os.environ["SECRET_KEY"]          # fails loudly if missing
ALGORITHM = os.environ["PWD_ENCRYPTION_ALGORITHM"]
TOKEN_TTL = timedelta(hours=1)

bearer = HTTPBearer()

def get_current_user(
  creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
) -> dict:
  try:
    return jwt.decode(
      creds.credentials,
      SECRET_KEY,
      algorithms=[ALGORITHM],
      options={"require": ["exp"]},
    )
  except jwt.ExpiredSignatureError:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired")
  except jwt.InvalidTokenError:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")


def require_role(*allowed: str):
  def checker(user: Annotated[dict, Depends(get_current_user)]) -> dict:
    if user["user_type"] not in allowed:
      raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")
    return user
  return checker