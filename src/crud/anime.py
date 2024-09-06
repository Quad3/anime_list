from sqlalchemy.orm import Session, joinedload
from fastapi.encoders import jsonable_encoder
from typing import Type

from schemas.anime import AnimeCreate
import models


def create_anime(
        session: Session,
        anime_create: AnimeCreate
) -> models.Anime:
    anime_create_dump = anime_create.model_dump()
    anime_from_to = jsonable_encoder(anime_create_dump.pop("from_to"))

    anime = models.Anime(**anime_create_dump)
    session.add(anime)
    session.commit()

    db_from_to = [models.AnimeFromTo(**from_to, anime_id=anime.uuid) for from_to in anime_from_to]
    session.add_all(db_from_to)
    session.commit()

    anime.from_to = db_from_to
    return anime


def get_anime_list(session: Session) -> list[Type[models.Anime]]:
    return session.query(models.Anime).options(joinedload(models.Anime.from_to)).all()
