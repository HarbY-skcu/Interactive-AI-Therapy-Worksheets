from typing import Protocol, Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer()

class GetCurrentUser(Protocol):
  def __call__(
    self,
    creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]
  ) -> dict:
    ...

class RequireRole(Protocol):
  def __call__(
    self,
    *allowed: str
  ) -> dict:
    ...