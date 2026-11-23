from typing import Protocol, Tuple
from src.backend.models.domain_models.encryption import EncryptedData

class Encrypter(Protocol):
  def encrypt_password(
    self,
    pwd: str,
  ) -> EncryptedData:
    pass

  def make_encrypted_token(
    self,
    user_id: str,
    user_type: str,
  ) -> str:
    pass