from typing import Protocol

from backend.models.domain_models.user_identity import UserInformation

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

  async def fetch_user(
    self,
    email: str,
  ) -> UserInformation:
    pass