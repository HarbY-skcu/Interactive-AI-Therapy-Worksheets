from sqlalchemy import ForeignKey, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from typing import List

from .base_model import Base
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
    ),
  )

  password: Mapped[str] = mapped_column(
    String(255),
    nullable=False,
  )
  email: Mapped[str] = mapped_column(
    unique = True,
    nullable = False,
  )
  user_type: Mapped[str] = mapped_column(
    nullable = False,
  )
  user_id: Mapped[str] = mapped_column(
    primary_key=True,
    unique = True,
    nullable = False,
  )

  @validates("user_type")
  def validate_type(self, _, user_type: str) -> str:
    return check_user_type(user_type)

  @validates("email")
  def validate_email(self, _, email: str) -> str:
    return check_email(email)

  @validates("user_id")
  def validate_user_id(self, _, user_id: str) -> str:
    return check_user_id(user_id)

  def __repr__(self):
    return f"<User_id {self.user_id}, email: {self.email}>"