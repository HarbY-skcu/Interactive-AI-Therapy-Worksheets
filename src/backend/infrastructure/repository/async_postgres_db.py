import asyncio
from sqlalchemy import select, insert
from sqlalchemy.orm import sessionmaker

from backend.domain.Ports.repository import CheckLoginRepository
from backend.models.domain_models.user_identity import UserInformation
from backend.models.data_models.base_model import Base
from backend.models.data_models.user_model import User
from sqlalchemy.ext.asyncio import (
  create_async_engine,
  AsyncEngine,
  async_sessionmaker,
  AsyncSession
)

from backend.models.domain_models.user_identity import UserInformation


class AsyncPostgresDatabase:

  def __init__(
    self,
    session_maker: async_sessionmaker,
    engine: AsyncEngine,
  ):
    self.engine = engine
    self.session_maker = session_maker

  @classmethod
  async def create(
    cls,
    db_url: str,
    engine: AsyncEngine | None = None
  ) -> AsyncPostgresDatabase:
    async_engine = engine if engine else create_async_engine(db_url)
    async_session = async_sessionmaker(
      async_engine,
      expire_on_commit=False
    )
    async with async_engine.begin() as conn:
      await conn.run_sync(Base.metadata.create_all) # type: ignore[arg-type]
    return cls(session_maker = async_session, engine = async_engine)

  async def close(self) -> None:
    await self.engine.dispose()

  async def check_if_credentials_are_allowed(
    self,
    password: str,
    email: str
  ) -> bool:
    async with self.session_maker() as session:
      stmt = select(User.email).where(User.email == email)
      email = await session.scalar(stmt)
    return bool(email)

  async def create_new_user(
    self,
    password: str,
    email: str,
    user_type: str,
    token: str,
    user_id: str
  ) -> None:
    async with self.session_maker() as session:
      stmt = insert(User).values(
        email = email,
        password = password,
        user_type = user_type,
        token = token,
        user_id = user_id
      )
      await session.execute(stmt)
      await session.commit()

  async def fetch_user(
    self,
    email: str
  ) -> UserInformation:
    async with self.session_maker() as session:
      stmt = select(User).where(User.email == email)
      result = await session.execute(stmt)
    user = result.first()
    return UserInformation(
      password = user["password"],
      email = user["email"],
      user_type = user["user_type"],
      token = user["token"],
      user_id = user["user_id"]
    )
