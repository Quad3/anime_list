import uuid
from fastapi import APIRouter, Depends, Path, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from database import get_db
from .schemas import (
    AnimeCreate,
    AnimeRead,
    AnimeUpdate,
    StartEndUpdate,
    StartEndRead,
    StartEndCreate
)
from . import service

router = APIRouter(
    tags=["Anime"]
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=AnimeRead)
async def create_anime(anime_create: AnimeCreate, session: Annotated[AsyncSession, Depends(get_db)]):
    anime = await service.create_anime(
        session=session,
        anime_create=anime_create
    )
    return anime


@router.get("/", response_model=list[AnimeRead])
async def get_anime_list(
        session: Annotated[AsyncSession, Depends(get_db)],
        limit: Annotated[int, Query(ge=1)] = 5,
        page: Annotated[int, Query(ge=1)] = 1
):
    anime_list = await service.get_anime_list(session=session, limit=limit, page=page)
    return anime_list


@router.get("/{id}", response_model=AnimeRead)
async def get_anime(
        session: Annotated[AsyncSession, Depends(get_db)],
        anime_id: Annotated[uuid.UUID, Path(alias="id")]
):
    anime = await service.get_anime(
        session=session,
        anime_id=anime_id
    )
    return anime


@router.patch("/{id}/update", response_model=AnimeUpdate)
async def update_anime(
        session: Annotated[AsyncSession, Depends(get_db)],
        anime_update: AnimeUpdate,
        anime_id: Annotated[uuid.UUID, Path(alias="id")]
):
    anime = await service.get_anime_by_id(session=session, anime_id=anime_id)
    if anime is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Anime with this id does not exist")

    updated_anime = await service.update_anime(
        session=session,
        anime_update=anime_update,
        anime=anime
    )
    return updated_anime


@router.patch("/{id}/update-start-end", response_model=StartEndRead, description="Updates last start_end dates")
async def update_anime_start_end(
        session: Annotated[AsyncSession, Depends(get_db)],
        anime_id: Annotated[uuid.UUID, Path(alias="id")],
        start_end_update: StartEndUpdate
):
    anime = await service.get_anime_by_id(session=session, anime_id=anime_id)
    if anime is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Anime with this id does not exist")

    updated_start_end = await service.update_anime_start_end(
        session=session,
        anime_id=anime_id,
        start_end_update=start_end_update
    )
    return updated_start_end


@router.post("/{id}/create-start-end", status_code=status.HTTP_201_CREATED, response_model=StartEndRead)
async def create_anime_start_end(
        session: Annotated[AsyncSession, Depends(get_db)],
        anime_id: Annotated[uuid.UUID, Path(alias="id")],
        start_end_create: StartEndCreate
):
    anime = await service.get_anime_by_id(session=session, anime_id=anime_id)
    if anime is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Anime with this id does not exist")

    start_end = await service.create_anime_start_end(
        session=session,
        anime=anime,
        start_end_create=start_end_create
    )
    return start_end
