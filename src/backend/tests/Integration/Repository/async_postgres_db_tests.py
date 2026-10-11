import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from backend.domain.Ports.repository import CheckLoginRepository


class TestAsyncPostgresDb:

  @pytest.mark.asyncio
  async def test_if_db_is_connnected(
    self,
    async_database: CheckLoginRepository
  ):
    try:
      async with async_database.engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result == 1
    except OperationalError as e:
        pytest.fail(f"Database connection failed: {e}")

  @pytest.mark.asyncio
  async def test_if_db_not_connected(
    self,
    disconnected_async_database: CheckLoginRepository
  ):
    with pytest.raises(OperationalError):
      async with disconnected_async_database.engine.connect() as conn:
        conn.execute(text("SELECT 1"))

  @pytest.mark.asyncio
  async def test_if_new_user_is_created(
    self,
    async_database: CheckLoginRepository,
    new_user: dict
  ):
    await async_database.create_new_user(
      **new_user
    )

    result = await async_database.fetch_user(
      email = new_user["email"],
    )

    assert all(entry in new_user.values() for entry in result)


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "potential_user",
    list_of_invalid_users
  )
  async def test_if_invalid_users_are_denied(
    self,
    async_database: CheckLoginRepository,
    potential_user: dict,
  ):
    with pytest.raises(ValueError) as exc_info:
      await self.async_database.create_new_user(**potential_user)

    assert exc_info.value in list_of_exceptions

  @pytest.mark.asyncio
  async def test_result_when_user_exists(
    self,
    populated_async_database: CheckLoginRepository,
    new_user: dict
  ):
    result = await populated_async_database.check_if_credentials_are_allowed(email=new_user["email"])
    assert not result
    assert isinstance(result, bool)

  @pytest.mark.asyncio
  async def test_result_when_user_does_not_exist(
    self,
    async_database: CheckLoginRepository,
    new_user: dict
  ):
    result = await async_database.check_if_credentials_are_allowed(email=new_user["email"])
    assert result
    assert isinstance(result, bool)
