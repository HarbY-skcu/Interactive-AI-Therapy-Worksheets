# validation.py
import os
import re
import uuid

import jwt
from jwt import InvalidTokenError
import dotenvx

dotenvx.load_dotenv("src/backend/config.env")

EMAIL_PATTERN = r'''[a-zA-Z0-9_+-]+(?:\.[a-zA-Z0-9_+-]+)*@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}'''
# Password max is 72: bcrypt rejects longer input, and the allowed charset is ASCII (1 char = 1 byte)
PASSWORD_PATTERN = r'''(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,72}'''
USER_TYPES = ("client", "therapist", "admin")
REQUIRED_CLAIMS = ["user_id", "user_type", "exp"]

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("PWD_ENCRYPTION_ALGORITHM")
_email_re = re.compile(EMAIL_PATTERN)
_password_re = re.compile(PASSWORD_PATTERN)

def check_email(value: str) -> str:
  if _email_re.fullmatch(value) is None:
      raise ValueError("Invalid email address")
  return value

def check_password(value: str) -> str:
  if _password_re.fullmatch(value) is None:
      raise ValueError("Invalid password")
  return value

def check_user_type(value: str) -> str:
  value = value.lower()
  if value not in USER_TYPES:
      raise ValueError(f"Not a valid user_type: {value}")
  return value

def check_user_id(value: str) -> str:
  try:
    parsed = uuid.UUID(value)
  except (ValueError, AttributeError, TypeError):
    raise ValueError("Invalid user_id") from None
  if str(parsed) != value.lower():
    raise ValueError("Invalid user_id")
  return str(parsed)

def check_token(token: str) -> str:
  try:
    claims = jwt.decode(
      token,
      SECRET_KEY,
      algorithms=[ALGORITHM],
      options={"require": REQUIRED_CLAIMS},
    )
  except InvalidTokenError:
    raise ValueError("Invalid token") from None

  try:
    check_user_id(claims["user_id"])
    check_user_type(claims["user_type"])
  except ValueError:
    raise ValueError("Invalid token") from None

  if set(claims) - set(REQUIRED_CLAIMS):
    raise ValueError("Invalid token")

  return claims["user_id"]