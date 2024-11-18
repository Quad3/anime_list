import uuid
import random
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from anime.models import Anime, AnimeStartEnd, State
from .utils import random_lower_string, random_start_end


async def create_random_anime(
        session: AsyncSession,
        start_end_len: int = 1,
        start_date: date | None = None,
        user_id: uuid.UUID | None = None,
) -> Anime:
    anime = Anime(
        name=random_lower_string(),
        rate=random.randint(1, 10),
        state=State.WATCHED,
        review=random_lower_string(256),
        user_id=user_id,
    )
    session.add(anime)

    db_start_end = []
    for start_end in random_start_end(start_end_len, start_date):
        db_start_end.append(AnimeStartEnd(
            start_date=start_end["start_date"],
            end_date=start_end["end_date"],
            anime_id=anime.uuid,
        ))

    session.add_all(db_start_end)
    anime.start_end = db_start_end
    await session.commit()
    await session.refresh(anime)
    return anime
