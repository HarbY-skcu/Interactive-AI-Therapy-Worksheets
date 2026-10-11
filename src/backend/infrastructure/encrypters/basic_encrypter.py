import os
from datetime import datetime, timezone, timedelta

import bcrypt
import uuid
import jwt

from backend.domain.Ports.encrypter import Encrypter
from backend.models.domain_models.encryption import EncryptedData


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

  def encrypt(
    self,
    pwd: str,
    user_type: str,
  ) -> EncryptedData:

    hashed_password = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    user_id = str(uuid.uuid4())
    token = jwt.encode(
      {
        "user_id": user_id,
        "user_type": user_type,
        "exp": datetime.now(timezone.utc) + self.TOKEN_TTL,
      },
      self.SECRET_KEY,
      algorithm= self.HASHED_PWD_ALGORITHM,
    )

    return EncryptedData(
      user_id = user_id,
      hashed_password = hashed_password,
      token = token,
    )