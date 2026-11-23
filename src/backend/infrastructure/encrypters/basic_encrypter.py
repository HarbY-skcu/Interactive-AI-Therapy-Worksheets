import os
from datetime import datetime, timezone, timedelta

import bcrypt
import uuid
import jwt

from backend.domain.Ports.encrypter import Encrypter
from backend.models.domain_models.encryption import EncryptedPassword


class BasicJWTEncrypter:
  def __init__(
    self,
    secret_key: str,
    hashed_pwd_algorithm: str,
    token_ttl: timedelta,
  ):
    self.SECRET_KEY = secret_key
    self.HASHED_PWD_ALGORITHM = hashed_pwd_algorithm
    self.TOKEN_TTL = token_ttl

  def encrypt_password(
    self,
    pwd: str,
  ) -> EncryptedPassword:
    hashed_password = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    user_id = str(uuid.uuid4())
    return EncryptedPassword(
      user_id = user_id,
      hashed_password = hashed_password,
    )

  def make_encrypted_token(
    self,
    user_id: str,
    user_type: str,
  ) -> str:
    return jwt.encode(
      {
        "user_id": user_id,
        "user_type": user_type.lower(),
        "exp": datetime.now(timezone.utc) + self.TOKEN_TTL,
      },
      self.SECRET_KEY,
      algorithm=self.HASHED_PWD_ALGORITHM,
    )