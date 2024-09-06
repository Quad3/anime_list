import datetime

from pydantic import BaseModel, Field, AliasChoices
from pydantic import ConfigDict
from pydantic.types import UUID4

from models import State


class FromToBase(BaseModel):
    from_: datetime.date = Field(alias="from", validation_alias=AliasChoices("from", "from_"))
    to: datetime.date | None


class FromToCreate(FromToBase):
    pass


class FromToRead(FromToBase):
    pass


class FromToUpdate(FromToBase):
    from_: datetime.date | None = Field(alias="from", validation_alias=AliasChoices("from", "from_"), default=None)
    to: datetime.date | None = None


class FromTo(FromToBase):
    id: int
    anime_id: UUID4


class AnimeBase(BaseModel):
    name: str
    state: State
    rate: int | None = Field(ge=1, le=10)
    review: str | None


class AnimeCreate(AnimeBase):
    from_to: list[FromToCreate]


class AnimeRead(AnimeBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    from_to: list[FromToRead]
    uuid: UUID4


class AnimeUpdate(AnimeBase):
    name: str | None = None
    state: State | None = None
    rate: int | None = Field(ge=1, le=10, default=None)
    review: str | None
