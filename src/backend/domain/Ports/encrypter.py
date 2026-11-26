from typing import Protocol, Tuple
from backend.models.domain_models.encryption import EncryptedPassword

class Encrypter(Protocol):
  def encrypt_password(
    self,
    pwd: str,
  ) -> EncryptedPassword:
    pass

  def make_encrypted_token(
    self,
    user_id: str,
    user_type: str,
  ) -> str:
    pass