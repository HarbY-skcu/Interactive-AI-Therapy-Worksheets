from base import Base
from pydantic import Field, ConfigDict

class RegisterRequest(Base):
  username: str = Field(
    min_length=8,
    max_length=40,
    description="Username of user account to create"
  )
  email: str = Field(description="Email address of new user account")
  password: str = Field(description="Encrypted password of potentially registered user")
  user_type: str = Field(
    description="Type of account they wish to create "
                "(Therapist, Client, Administrator)"
  )

  model_config = ConfigDict(
    strict=True,
    extra = "forbid"
  )

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