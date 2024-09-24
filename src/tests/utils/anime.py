import random
from sqlalchemy.ext.asyncio import AsyncSession

from anime.models import Anime, AnimeStartEnd
from .utils import random_lower_string, random_start_end
from anime.models import State


async def create_random_anime(
        session: AsyncSession,
        start_end_len: int = 1
) -> Anime:
    anime = Anime(
        name=random_lower_string(),
        rate=random.randint(1, 10),
        state=State.WATCHED,
        review=random_lower_string(256)
    )
    session.add(anime)

    db_start_end = []
    for start_end in random_start_end(start_end_len):
        db_start_end.append(AnimeStartEnd(
            start_date=start_end["start_date"],
            end_date=start_end["end_date"],
            anime_id=anime.uuid
        ))

    session.add_all(db_start_end)
    anime.start_end = db_start_end
    await session.commit()
    await session.refresh(anime)

    return anime
