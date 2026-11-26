from typing import Annotated
import re

from backend.models.api_schemas.base import Base
from pydantic import Field, ConfigDict, SecretStr, model_validator, ValidationError
from backend.domain.service.check_input_service import (
  check_password,
  check_email,
  check_user_type,
  check_token,
  check_user_id,
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
    self.user_type = check_user_type(self.user_type)
    return self

  model_config = ConfigDict(
    strict=True,
    extra = "forbid"
  )

class RegisterResponse(Base):
  user_id: str = Field(description= "User's unique ID")
  user_type: str = Field(description="Type of account they wish to create")

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

class LoginResponse(Base):
  user_id: str = Field(
    description="User's unique ID"
  )
  token: str = Field(
    description="Token of logged in user"
  )

  @model_validator(mode = "after")
  def verify_valid_token(
    self,
  ) -> LoginResponse:
    check_token(self.token)
    return self

  @model_validator(mode = "after")
  def verify_valid_user_id(
    self
  ) -> LoginResponse:
    check_user_id(self.user_id)
    return self