import uuid
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import Annotated

from database import get_db
from schemas.anime import AnimeCreate, AnimeRead, AnimeUpdate
from crud import anime as anime_crud


router = APIRouter(
    tags=["Anime"]
)


@router.post("/create", response_model=AnimeRead)
def create_anime(anime_create: AnimeCreate, session: Annotated[Session, Depends(get_db)]):
    anime = anime_crud.create_anime(
        session=session,
        anime_create=anime_create
    )

    return anime


@router.get("/", response_model=list[AnimeRead])
def get_anime_list(session: Annotated[Session, Depends(get_db)]):
    anime_list = anime_crud.get_anime_list(session=session)
    return anime_list


@router.get("/{id}", response_model=AnimeRead)
def get_anime_list(session: Annotated[Session, Depends(get_db)], anime_id: Annotated[uuid.UUID, Path(alias="id")]):
    anime = anime_crud.get_anime(session=session, anime_id=anime_id)
    return anime


@router.patch("/update/{id}", response_model=AnimeUpdate)
def update_anime(
        anime_update: AnimeUpdate,
        session: Annotated[Session, Depends(get_db)],
        anime_id: Annotated[uuid.UUID, Path(alias="id")]
):
    updated_anime = anime_crud.update_anime(session=session, anime_update=anime_update, anime_id=anime_id)
    return updated_anime
