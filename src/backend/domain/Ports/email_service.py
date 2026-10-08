from typing import Protocol

class EmailService(Protocol):

  async def verify_email(
    self,
    email: str,
  ) -> None:
    pass

