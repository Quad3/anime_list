from sqlalchemy.orm import Session

from src.schemas.anime import AnimeCreate
from src.models import Anime


def create_anime(
        session: Session,
        anime_create: AnimeCreate
) -> Anime:
    anime = Anime(**anime_create)

    session.add(anime)
    session.commit()

    return anime
