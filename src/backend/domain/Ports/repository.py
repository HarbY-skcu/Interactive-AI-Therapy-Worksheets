from typing import Protocol

class CheckLoginRepository(Protocol):

  async def check_if_credentials_are_allowed(
    self,
    password: str,
    email: str,
  ) -> bool:
    pass

  async def create_new_user(
    self,
    password: str,
    email: str,
    user_type: str,
    token: str,
    user_id: str
  ) -> None:
    pass

  async def check_if_user_exists(
    self,
    email: str,
  ) -> bool:
    # The output of this should be a user object
    pass