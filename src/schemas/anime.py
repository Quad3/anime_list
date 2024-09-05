import datetime

from pydantic import BaseModel, Field, AliasChoices
from pydantic import ConfigDict
from pydantic.types import UUID4

from src.models import State


class FromToBase(BaseModel):
    from_: datetime.date = Field(alias="from", validation_alias=AliasChoices("from", "from_"))
    to: datetime.date | None


class FromToCreate(FromToBase):
    pass


class FromToRead(FromToBase):
    pass


class FromTo(FromToBase):
    id: int
    anime_id: UUID4


class AnimeBase(BaseModel):
    name: str
    state: State
    rate: int | None = Field(ge=1, le=10)
    review: str | None
    from_to: list[FromTo]


class AnimeCreate(AnimeBase):
    from_to: list[FromToCreate]


class AnimeRead(AnimeBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    from_to: list[FromToRead]
    uuid: UUID4
