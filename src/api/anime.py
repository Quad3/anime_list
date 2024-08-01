
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from src.database import get_db
from src.schemas.anime import AnimeCreate, AnimeRead
from src.crud import anime as anime_crud


router = APIRouter(
    tags=["Anime"]
)


@router.post("/create", response_model=AnimeRead)
def create_anime(anime_create: AnimeCreate, session: Session = Depends(get_db)):
    anime = anime_crud.create_anime(
        session=session,
        anime_create=jsonable_encoder(anime_create)
    )

    return anime
