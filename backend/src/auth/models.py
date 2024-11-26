import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    uuid = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    anime = relationship("Anime", back_populates="user")


from anime.models import Anime # noqa: E402
