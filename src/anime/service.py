import uuid
import sqlalchemy.sql.functions as func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, desc
from fastapi import HTTPException, status

from .schemas import (
    AnimeCreate,
    AnimeUpdate,
    StartEndUpdate,
    StartEndCreate
)
from . import models
from .utils import is_start_end_valid


async def get_anime_by_id(session: AsyncSession, anime_id: uuid.UUID):
    stmt = select(models.Anime).filter(models.Anime.uuid == anime_id)
    result = await session.scalars(stmt)
    return result.first()


async def create_anime(
        session: AsyncSession,
        anime_create: AnimeCreate
) -> models.Anime:
    anime_create_dump = anime_create.model_dump()
    anime_start_end = anime_create_dump.pop("start_end")

    anime = models.Anime(**anime_create_dump)

    async with session.begin():
        session.add(anime)

        db_start_end = []
        for start_end in anime_start_end:
            start_date = start_end.get("start_date")
            end_date = start_end.get("end_date")
            if start_date and end_date:
                is_start_end_valid(start_date, end_date)

            db_start_end.append(models.AnimeStartEnd(
                start_date=start_date,
                end_date=end_date,
                anime_id=anime.uuid)
            )
            anime.start_end.append(db_start_end[-1])

        session.add_all(db_start_end)

    anime.start_end = db_start_end
    return anime


async def get_anime_list(session: AsyncSession, limit: int, page: int):
    subq = (
        select(models.AnimeStartEnd.anime_id)
        .group_by(models.AnimeStartEnd.anime_id)
        .order_by(func.min(models.AnimeStartEnd.start_date))
        .limit(limit)
        .offset((page - 1) * limit)
        .subquery()
    )
    stmt = (
        select(models.Anime)
        .join(subq)
        .options(joinedload(models.Anime.start_end))
    )
    result = await session.execute(stmt)
    anime_list = result.scalars().unique().all()
    if not anime_list:
        if page == 1:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="There is no anime yet")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Out-of-Range page request")

    return anime_list


async def get_anime(session: AsyncSession, anime_id: uuid.UUID):
    stmt = select(models.Anime) \
        .options(joinedload(models.Anime.start_end)) \
        .filter(models.Anime.uuid == anime_id)
    result = await session.scalars(stmt)
    anime = result.unique().first()
    if anime is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Anime not found")

    return anime


async def update_anime(
        session: AsyncSession,
        anime_update: AnimeUpdate,
        anime: models.Anime
):
    anime_update_data = anime_update.model_dump(exclude_none=True)
    for key, value in anime_update_data.items():
        setattr(anime, key, value)

    session.add(anime)
    await session.commit()

    return anime


async def update_anime_start_end(
        session: AsyncSession,
        start_end_update: StartEndUpdate,
        anime_id: uuid.UUID
):
    stmt = select(models.AnimeStartEnd) \
        .filter(models.AnimeStartEnd.anime_id == anime_id) \
        .order_by(desc(models.AnimeStartEnd.start_date))
    result = await session.scalars(stmt)
    db_start_end = result.unique().first()

    if not db_start_end:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

    start_date = start_end_update.start_date if start_end_update.start_date else db_start_end.start_date
    end_date = start_end_update.end_date if start_end_update.end_date else db_start_end.end_date
    is_start_end_valid(start_date, end_date)

    for key, value in start_end_update.model_dump(exclude_none=True).items():
        setattr(db_start_end, key, value)

    session.add(db_start_end)
    await session.commit()

    return db_start_end


async def create_anime_start_end(
        session: AsyncSession,
        start_end_create: StartEndCreate,
        anime: models.Anime
):
    start_end = models.AnimeStartEnd(**start_end_create.model_dump(), anime_id=anime.uuid)
    if start_end.start_date and start_end.end_date:
        is_start_end_valid(start_end.start_date, start_end.end_date)
    session.add(start_end)
    await session.commit()

    return start_end
