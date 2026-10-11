from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates
from base_model import Base
import re
from backend.domain.service.check_input_service import (
  check_password,
  check_email,
  check_user_type,
  check_token,
  check_user_id
)

class User(Base):
  __tablename__ = 'user_information'
  __table_args__ = (
    CheckConstraint(
      "user_type IN ('client', 'therapist', 'admin')",
      name = "ck_user_information_user_type"
    )
  )

  password: Mapped[str] = mapped_column()
  email: Mapped[str] = mapped_column(
    primary_key = True,
    unique = True
  )
  user_type: Mapped[str] = mapped_column()
  token: Mapped[str] = mapped_column(unique = True)
  user_id: Mapped[str] = mapped_column(
    ForeignKey("user_data.id"),
    unique = True
  )

  @validates("user_type")
  def validate_type(self, _, user_type: str) -> str:
    return check_user_type(user_type)

  @validates("email")
  def validate_email(self, _, email: str) -> str:
    return check_email(email)

  @validates("password")
  def validate_password(self, _, password: str) -> str:
    return check_password(password)

  @validates("token")
  def validate_token(self, _, token: str) -> str:
    return check_token(token)

  @validates("user_id")
  def validate_user_id(self, _, user_id: str) -> str:
    return check_user_id(user_id)

  def __repr__(self):
    return f"<User_id {self.user_id}, email: {self.email}>"