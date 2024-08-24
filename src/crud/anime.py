from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from src.schemas.anime import AnimeCreate
from src import models


def create_anime(
        session: Session,
        anime_create: AnimeCreate
) -> models.Anime:
    anime = models.Anime(**jsonable_encoder(anime_create))

    session.add(anime)
    session.commit()

    return anime


def get_anime_list(session: Session):
    return session.query(models.Anime).all()
