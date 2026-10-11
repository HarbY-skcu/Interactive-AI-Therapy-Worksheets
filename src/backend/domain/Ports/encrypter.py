from typing import Protocol, Tuple
from src.backend.models.domain_models.encryption import EncryptedData

class Encrypter(Protocol):
  def encrypt(
    self,
    pwd: str,
    user_type: str,
  ) -> EncryptedData:
    pass