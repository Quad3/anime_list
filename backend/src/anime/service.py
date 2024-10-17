import uuid

import sqlalchemy.sql.functions as func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, func
from fastapi import HTTPException, status

from .schemas import (
    AnimeCreate,
    AnimeUpdate,
    StartEndUpdate,
    StartEndCreate,
    StartEndListRead,
)
from . import models
from .utils import is_start_end_valid_or_raise, fill_start_end_if_valid, determine_anime_state
from auth.models import User


async def get_anime_by_id_or_404(session: AsyncSession, anime_id: uuid.UUID):
    stmt = select(models.Anime).filter(models.Anime.uuid == anime_id)
    result = await session.scalars(stmt)
    anime = result.first()
    if anime is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Anime with this id does not exist")

    return anime


async def create_anime(
        session: AsyncSession,
        current_user: User,
        anime_create: AnimeCreate,
) -> models.Anime:
    anime_create_dump = anime_create.model_dump()
    start_end_in: list[StartEndCreate] | None = anime_create_dump.pop("start_end", None)

    anime = models.Anime(
        **anime_create_dump,
        state=determine_anime_state(start_end_in),
        user_id=current_user.uuid,
    )

    async with session.begin_nested():
        session.add(anime)

        db_start_end = fill_start_end_if_valid(start_end_in)
        for start_end in db_start_end:
            start_end.anime_id = anime.uuid
        anime.start_end = db_start_end

        await session.commit()

    return anime


async def get_anime_list(
        session: AsyncSession,
        current_user: User,
        limit: int,
        page: int,
):
    count_stmt = (
        select(func.count())
        .select_from(models.Anime)
        .where(models.Anime.user_id == current_user.uuid)
    )
    count_result = await session.scalars(count_stmt)
    count = count_result.first()
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
        .where(models.Anime.user_id == current_user.uuid)
    )
    result = await session.execute(stmt)
    anime_list = result.scalars().unique().all()
    return {"data": anime_list, "count": count}


async def get_anime(session: AsyncSession, current_user: User, anime_id: uuid.UUID):
    stmt = (
        select(models.Anime)
        .options(joinedload(models.Anime.start_end))
        .filter(models.Anime.uuid == anime_id)
    )
    result = await session.scalars(stmt)
    anime = result.unique().first()
    if anime is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Anime with this id does not exist")
    if not current_user.is_superuser and anime.user_id != current_user.uuid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    return anime


async def update_anime(
        session: AsyncSession,
        anime_update: AnimeUpdate,
        anime: models.Anime,
):
    anime_update_data = anime_update.model_dump(exclude_none=True)
    for key, value in anime_update_data.items():
        setattr(anime, key, value)

    session.add(anime)
    await session.commit()
    await session.refresh(anime)
    return anime


async def update_anime_start_end(
        session: AsyncSession,
        current_user: User,
        start_end_update: StartEndUpdate,
        anime_id: uuid.UUID,
):
    stmt = (
        select(models.Anime)
        .options(joinedload(models.Anime.start_end))
        .filter(models.Anime.uuid == anime_id)
    )
    result = await session.scalars(stmt)
    anime: models.Anime = result.unique().first()
    if not anime:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Anime with this id does not exist")
    if anime.user_id != current_user.uuid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    if not anime.start_end:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Data not found")
    db_start_end: models.AnimeStartEnd = anime.start_end[-1]

    start_date = start_end_update.start_date if start_end_update.start_date else db_start_end.start_date
    end_date = start_end_update.end_date if start_end_update.end_date else db_start_end.end_date
    is_start_end_valid_or_raise(start_date, end_date)

    for key, value in start_end_update.model_dump(exclude_none=True).items():
        setattr(db_start_end, key, value)

    session.add(db_start_end)
    await session.commit()
    await session.refresh(db_start_end)
    return db_start_end


async def create_anime_start_end(
        session: AsyncSession,
        start_end_create: StartEndCreate,
        anime: models.Anime,
):
    start_end = models.AnimeStartEnd(**start_end_create.model_dump(), anime_id=anime.uuid)
    if start_end.start_date and start_end.end_date:
        is_start_end_valid_or_raise(start_end.start_date, start_end.end_date)
    session.add(start_end)
    await session.commit()
    return start_end


async def get_start_end_list(
        session: AsyncSession,
        current_user: User,
):
    stmt = (
        select(models.AnimeStartEnd)
        .join(models.Anime)
        .options(joinedload(models.AnimeStartEnd.anime))
        .filter(models.Anime.user_id == current_user.uuid)
        .order_by(models.AnimeStartEnd.start_date)
    )
    result = await session.scalars(stmt)
    start_end_list = result.unique().all()
    start_end_list_read = []
    for start_end in start_end_list:
        start_end_list_read.append(StartEndListRead(
            start_date=start_end.start_date,
            end_date=start_end.end_date,
            name=start_end.anime.name,
            rate=start_end.anime.rate,
            state=start_end.anime.state,
            review=start_end.anime.review,
            user_id=start_end.anime.user_id,
            anime_id=start_end.anime_id,
        ))
    return start_end_list_read
