import uuid
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from database import get_db
from schemas.anime import AnimeCreate, AnimeRead, AnimeUpdate, StartEndUpdate, StartEndRead, StartEndCreate
from crud import anime as anime_crud


router = APIRouter(
    tags=["Anime"]
)


@router.post("/create", response_model=AnimeRead)
async def create_anime(anime_create: AnimeCreate, session: Annotated[AsyncSession, Depends(get_db)]):
    anime = await anime_crud.create_anime(
        session=session,
        anime_create=anime_create
    )
    return anime


@router.get("/", response_model=list[AnimeRead])
async def get_anime_list(session: Annotated[AsyncSession, Depends(get_db)]):
    anime_list = await anime_crud.get_anime_list(session=session)
    return anime_list


@router.get("/{id}", response_model=AnimeRead)
async def get_anime(
        session: Annotated[AsyncSession, Depends(get_db)],
        anime_id: Annotated[uuid.UUID, Path(alias="id")]
):
    anime = await anime_crud.get_anime(
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
    updated_anime = await anime_crud.update_anime(
        session=session,
        anime_update=anime_update,
        anime_id=anime_id
    )
    return updated_anime


@router.patch("/{id}/update-start-end", response_model=StartEndRead, description="Updates last start_end dates")
async def update_anime_start_end(
        session: Annotated[AsyncSession, Depends(get_db)],
        anime_id: Annotated[uuid.UUID, Path(alias="id")],
        start_end_update: StartEndUpdate
):
    updated_start_end = await anime_crud.update_anime_start_end(
        session=session,
        anime_id=anime_id,
        start_end_update=start_end_update
    )
    return updated_start_end


@router.post("/{id}/create-start-end", response_model=StartEndRead)
async def create_anime_start_end(
        session: Annotated[AsyncSession, Depends(get_db)],
        anime_id: Annotated[uuid.UUID, Path(alias="id")],
        start_end_create: StartEndCreate
):
    start_end = await anime_crud.create_anime_start_end(
        session=session,
        anime_id=anime_id,
        start_end_create=start_end_create
    )
    return start_end
