import uuid
from typing import Annotated

from fastapi import APIRouter, Path, HTTPException, status, Query

from .schemas import (
    AnimeCreate,
    AnimeRead,
    AnimeUpdate,
    AnimeListRead,
    StartEndUpdate,
    StartEndRead,
    StartEndCreate,
)
from . import service
from auth.deps import SessionDep, CurrentUser


router = APIRouter(
    tags=["Anime"],
    prefix="/anime",
)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=AnimeRead,
)
async def create_anime(
        anime_create: AnimeCreate,
        session: SessionDep,
        current_user: CurrentUser,
):
    anime = await service.create_anime(
        session=session,
        current_user=current_user,
        anime_create=anime_create
    )
    return anime


@router.get("/", response_model=AnimeListRead)
async def get_anime_list(
        session: SessionDep,
        current_user: CurrentUser,
        limit: Annotated[int, Query(ge=1)] = 5,
        page: Annotated[int, Query(ge=1)] = 1,
):
    anime_list = await service.get_anime_list(
        session=session,
        current_user=current_user,
        limit=limit,
        page=page,
    )
    if not anime_list["count"]:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="There is no anime yet")
    if not anime_list["data"]:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Out-of-Range page request")
    return anime_list


@router.get("/{id}", response_model=AnimeRead)
async def get_anime(
        session: SessionDep,
        current_user: CurrentUser,
        anime_id: Annotated[uuid.UUID, Path(alias="id")],
):
    anime = await service.get_anime(
        session=session,
        current_user=current_user,
        anime_id=anime_id,
    )
    return anime


@router.patch("/{id}/update", response_model=AnimeUpdate)
async def update_anime(
        session: SessionDep,
        current_user: CurrentUser,
        anime_update: AnimeUpdate,
        anime_id: Annotated[uuid.UUID, Path(alias="id")],
):
    anime = await service.get_anime_by_id_or_404(session=session, anime_id=anime_id)
    if anime.user_id != current_user.uuid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")

    updated_anime = await service.update_anime(
        session=session,
        anime_update=anime_update,
        anime=anime
    )
    return updated_anime


@router.patch(
    "/{id}/update-start-end",
    response_model=StartEndRead,
    description="Updates last start_end dates",
)
async def update_anime_start_end(
        session: SessionDep,
        current_user: CurrentUser,
        anime_id: Annotated[uuid.UUID, Path(alias="id")],
        start_end_update: StartEndUpdate,
):
    updated_start_end = await service.update_anime_start_end(
        session=session,
        current_user=current_user,
        anime_id=anime_id,
        start_end_update=start_end_update,
    )
    return updated_start_end


@router.post(
    "/{id}/create-start-end",
    status_code=status.HTTP_201_CREATED,
    response_model=StartEndRead,
)
async def create_anime_start_end(
        session: SessionDep,
        anime_id: Annotated[uuid.UUID, Path(alias="id")],
        start_end_create: StartEndCreate,
):
    anime = await service.get_anime_by_id_or_404(session=session, anime_id=anime_id)

    start_end = await service.create_anime_start_end(
        session=session,
        anime=anime,
        start_end_create=start_end_create,
    )
    return start_end
