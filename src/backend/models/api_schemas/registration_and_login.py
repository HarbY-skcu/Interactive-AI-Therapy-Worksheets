from backend.models.api_schemas.base import Base
from pydantic import Field, ConfigDict, SecretStr

class RegisterRequest(Base):
  email: str = Field(description="Email address of new user account")
  password: SecretStr = Field(description="plaintext password of potentially registered user")
  user_type: str = Field(
    description="Type of account they wish to create "
                "(Therapist, Client, Administrator)"
  )

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
  password: str = Field(
    description="Encrypted password of potentially registered user"
  )

  model_config = ConfigDict(
    strict=True,
    extra = "forbid"
  )