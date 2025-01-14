import datetime

from pydantic import BaseModel, Field
from pydantic import ConfigDict
from pydantic.types import UUID4

from .models import State


class StartEndBase(BaseModel):
    start_date: datetime.date
    end_date: datetime.date | None = None


class StartEndCreate(StartEndBase):
    pass


class StartEndRead(StartEndBase):
    pass


class StartEndUpdate(BaseModel):
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None


class StartEnd(StartEndBase):
    id: int
    anime_id: UUID4


class AnimeBase(BaseModel):
    name: str
    state: State
    rate: int | None = Field(ge=1, le=10)
    review: str | None


class AnimeCreate(BaseModel):
    name: str
    rate: int | None = Field(ge=1, le=10)
    review: str | None
    start_end: list[StartEndCreate] | None = None


class AnimeRead(AnimeBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    start_end: list[StartEndRead]
    user_id: UUID4
    uuid: UUID4


class AnimeListRead(BaseModel):
    data: list[AnimeRead]
    count: int


class AnimeUpdate(BaseModel):
    name: str | None = None
    state: State | None = None
    rate: int | None = Field(ge=1, le=10, default=None)
    review: str | None = None


class StartEndListRead(StartEndRead, AnimeBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    user_id: UUID4
    anime_id: UUID4
