from dataclasses import dataclass

@dataclass(frozen=True)
class EncryptedPassword:
  hashed_password: bytes
  user_id: str

