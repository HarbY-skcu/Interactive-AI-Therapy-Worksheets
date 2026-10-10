from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates
from base_model import Base
import re

class User(Base):
  __tablename__ = 'user_information'

  password: Mapped[str] = mapped_column(unique = True)
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
    if user_type.lower() not in ["client", "therapist", "admin"]:
      raise ValueError(f"Not a valid user_type: {user_type}")
    return user_type

  @validates("email")
  def validate_email(self, _, email: str) -> str:
    if not re.match(
      r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
      email
    ):
      raise ValueError(f"Invalid email address: {email}")
    return email

  def __repr__(self):
    return f"<User_id {self.user_id}, email: {self.email}>"