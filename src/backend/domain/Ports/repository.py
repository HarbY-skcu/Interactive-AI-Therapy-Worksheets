from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncEngine

from backend.models.domain_models.user_identity import UserInformation

class CheckLoginRepository(Protocol):

  @classmethod
  async def create(
    cls,
    db_url: str,
    engine: AsyncEngine | None = None
  ):
    pass

  async def check_if_credentials_are_allowed(
    self,
    email: str,
  ) -> bool:
    pass

  async def create_new_user(
    self,
    password: str,
    email: str,
    user_type: str,
    user_id: str
  ) -> None:
    pass

  async def fetch_user(
    self,
    email: str,
  ) -> UserInformation:
    pass