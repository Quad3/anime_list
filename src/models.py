import uuid
import enum
from sqlalchemy import Column, String, UUID, Integer, Date, ForeignKey
from sqlalchemy.types import Enum
from sqlalchemy.orm import relationship

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

    from_to = relationship("AnimeFromTo", back_populates="anime_id")


class AnimeFromTo(Base):
    __tablename__ = "anime_from_to"

    id = Column(Integer, primary_key=True)
    from_ = Column(Date, name="from")
    to = Column(Date, nullable=True)
    anime_id = Column(UUID, ForeignKey("anime.uuid"))

    anime = relationship("Anime", back_populates="from_to")
