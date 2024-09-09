import uuid
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import select
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import Type

from schemas.anime import AnimeCreate, AnimeRead, AnimeUpdate
import models


def create_anime(
        session: Session,
        anime_create: AnimeCreate
) -> models.Anime:
    anime_create_dump = anime_create.model_dump()
    anime_start_end = jsonable_encoder(anime_create_dump.pop("start_end"))

    anime = models.Anime(**anime_create_dump)
    session.add(anime)
    session.commit()

    db_start_end = [models.AnimeStartEnd(**start_end, anime_id=anime.uuid) for start_end in anime_start_end]
    session.add_all(db_start_end)
    session.commit()

    anime.start_end = db_start_end
    return anime


def get_anime_list(session: Session):
    stmt = select(models.Anime) \
        .options(joinedload(models.Anime.start_end))
    result = session.scalars(stmt).unique().all()
    return result


def get_anime(session: Session, anime_id: uuid.UUID) -> Type[AnimeRead]:
    stmt = select(models.Anime) \
        .options(joinedload(models.Anime.start_end)) \
        .filter(models.Anime.uuid == anime_id)
    result = session.scalars(stmt).unique().first()
    return result


def update_anime(
        session: Session,
        anime_update: AnimeUpdate,
        anime_id: uuid.UUID
) -> Type[models.Anime]:
    db_anime = session.query(models.Anime).filter(models.Anime.uuid == anime_id).first()
    if not db_anime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Anime not found")

    anime_update_data = anime_update.model_dump(exclude_none=True)
    for key, value in anime_update_data.items():
        setattr(db_anime, key, value)

    session.add(db_anime)
    session.commit()

    return db_anime
