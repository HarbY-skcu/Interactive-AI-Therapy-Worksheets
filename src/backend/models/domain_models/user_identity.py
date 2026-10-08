from dataclasses import dataclass


@dataclass(frozen=True)
class UserInformation():
  password: str
  email: str
  user_type: str
  token: str
  user_id: str