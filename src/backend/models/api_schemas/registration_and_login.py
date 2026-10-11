from typing import Annotated
import re

from backend.models.api_schemas.base import Base
from pydantic import Field, ConfigDict, SecretStr, model_validator, ValidationError
from backend.domain.service.check_input_service import (
  check_password,
  check_email,
  check_user_type
)

class RegisterRequest(Base):
  email: str = Field(description="Email address of new user account")
  password: SecretStr = Field(description="plaintext password of potentially registered user")
  user_type: str = Field(
    description="Type of account they wish to create "
                "(Therapist, Client, Admin)"
  )

  @model_validator(mode = "after")
  def verify_valid_email_address(
    self
  ) -> RegisterRequest:
    check_email(self.email)
    return self

  @model_validator(mode = "after")
  def verify_valid_password(
    self,
  ) -> RegisterRequest:
    real_pwd = self.password.get_secret_value()
    check_password(real_pwd)
    return self

  @model_validator(mode = "after")
  def verify_valid_user_type(
    self,
  ) -> RegisterRequest:
    check_user_type(self.user_type.lower())
    return self

  model_config = ConfigDict(
    strict=True,
    extra = "forbid"
  )

class RegisterRequestResponse(Base):
  token: str = Field(description = "Generated Token for valid user")
  user_id: str = Field(description="User's unique ID")
  user_type: str = Field(description="Type of account they wish to create ")

class LoginRequest(Base):
  email: str = Field(
    description="Email address of new user account"
  )
  password: SecretStr = Field(
    description="Encrypted password of potentially registered user"
  )

  @model_validator(mode = "after")
  def verify_valid_email_address(
    self
  ) -> LoginRequest:
    check_email(self.email)
    return self

  @model_validator(mode = "after")
  def verify_valid_password(
    self,
  ) -> LoginRequest:
    real_pwd = self.password.get_secret_value()
    check_password(real_pwd)
    return self

  model_config = ConfigDict(
    strict=True,
    extra = "forbid"
  )