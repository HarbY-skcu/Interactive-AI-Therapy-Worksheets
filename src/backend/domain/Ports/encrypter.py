from typing import Protocol, Tuple
from src.backend.models.domain_models.encryption import EncryptedData

class Encrypter(Protocol):
  def encrypt(
    self,
    pwd: str
  ) -> EncryptedData:
    pass

  # hashed_password = bcrypt.hashpw(proposed_user.password.encode(), bcrypt.gensalt())
  # user_id = str(uuid.uuid4())
  # token = jwt.encode(
  #   {
  #     "user_id": user_id,
  #     "user_type": user_type,
  #     "exp": datetime.now(timezone.utc) + TOKEN_TTL,
  #   },
  #   os.getenv("SECRET_KEY"),
  #   algorithm= os.getenv("PWD_ENCRYPTION_ALGORITHM")
  # )
  #
  # !!! Put into class that realizes Encrypter !!!