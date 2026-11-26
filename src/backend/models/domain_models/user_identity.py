from dataclasses import dataclass


@dataclass(frozen=True)
class UserInformation():
  password: str
  email: str
  user_type: str
  user_id: str
  token: str | None = None

  def __iter__(self):
    return iter([self.user_id, self.email, self.user_type, self.password, self.token])