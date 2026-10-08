from dataclasses import dataclass

@dataclass(frozen=True)
class EncryptedData:
  hashed_password: bytes
  user_id: str
  token: str
