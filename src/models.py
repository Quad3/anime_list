import uuid
import enum
from sqlalchemy import Column, JSON, String, UUID, Integer
from sqlalchemy.types import Enum

from database import Base


class State(str, enum.Enum):
    WATCHING = "WATCHING"
    WATCHED = "WATCHED"
    DROPPED = "DROPPED"


class Anime(Base):
    __tablename__ = "anime"

    uuid = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False, unique=True)
    state = Column(Enum(State), default="WATCHING")
    rate = Column(Integer, nullable=True)
    review = Column(String(4096), nullable=True)
    from_to = Column(JSON, nullable=False)
