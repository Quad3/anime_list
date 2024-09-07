import datetime

from pydantic import BaseModel, Field
from pydantic import ConfigDict
from pydantic.types import UUID4

from models import State


class StartEndBase(BaseModel):
    start_date: datetime.date
    end_date: datetime.date | None


class StartEndCreate(StartEndBase):
    pass


class StartEndRead(StartEndBase):
    pass


class StartEndUpdate(StartEndBase):
    end_date: datetime.date | None = None


class StartEnd(StartEndBase):
    id: int
    anime_id: UUID4


class AnimeBase(BaseModel):
    name: str
    state: State
    rate: int | None = Field(ge=1, le=10)
    review: str | None


class AnimeCreate(AnimeBase):
    start_end: list[StartEndCreate]


class AnimeRead(AnimeBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    start_end: list[StartEndRead]
    uuid: UUID4


class AnimeUpdate(AnimeBase):
    name: str | None = None
    state: State | None = None
    rate: int | None = Field(ge=1, le=10, default=None)
    review: str | None = None
