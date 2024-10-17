import uuid
import enum
from sqlalchemy import Column, String, UUID, Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.types import Enum
from sqlalchemy.orm import relationship

from database import Base


class State(str, enum.Enum):
    WATCHING = "WATCHING"
    WATCHED = "WATCHED"
    DROPPED = "DROPPED"
    PLAN_TO_WATCH = "PLAN_TO_WATCH"


class Anime(Base):
    __tablename__ = "anime"

    uuid = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    state = Column(Enum(State), default=State.WATCHING)
    rate = Column(Integer, nullable=True)
    review = Column(String(4096), nullable=True)
    user_id = Column(UUID, ForeignKey("users.uuid"))

    start_end = relationship(
        "AnimeStartEnd",
        back_populates="anime",
        order_by="AnimeStartEnd.start_date",
    )
    user = relationship("User", back_populates="anime")

    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='anime_name_uc'),
    )


class AnimeStartEnd(Base):
    __tablename__ = "anime_start_end"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    anime_id = Column(UUID, ForeignKey("anime.uuid"))

    anime = relationship("Anime", back_populates="start_end")
