from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

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


def get_anime_list(session: Session):
    return session.query(models.Anime).join(models.AnimeFromTo).all()
