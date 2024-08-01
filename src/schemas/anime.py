import datetime

from pydantic import BaseModel, Field
from pydantic import ConfigDict
from pydantic.types import UUID4

from src.models import State


class FromTo(BaseModel):
    from_: datetime.date
    to: datetime.date | None


class AnimeBase(BaseModel):
    name: str
    state: State
    rate: int = Field(ge=1, le=10)
    review: str
    from_to: list[FromTo]


class AnimeCreate(AnimeBase):
    pass


class AnimeRead(AnimeBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    uuid: UUID4
