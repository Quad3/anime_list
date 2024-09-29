import random
import string
from datetime import date, timedelta
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from anime.models import Anime, AnimeStartEnd, State


def random_lower_string(k: int = 16) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))


def random_start_end(k: int = 1, start_date: date = None) -> list[dict[date | Any]]:
    res = []
    if not start_date:
        start_date = (
                date(year=random.randint(2010, 2024), month=1, day=1)
                + timedelta(days=random.randint(1, 365))
        )
    for i in range(k):
        end_date = start_date + timedelta(days=random.randint(1, 60))
        res.append({
            "start_date": start_date,
            "end_date": end_date
        })
        start_date = end_date + timedelta(days=random.randint(90, 180))
    return res


async def create_random_anime(
        session: AsyncSession,
        start_end_len: int = 1,
        start_date: date = None,
) -> Anime:
    anime = Anime(
        name=random_lower_string(),
        rate=random.randint(1, 10),
        state=State.WATCHED,
        review=random_lower_string(256)
    )
    session.add(anime)

    db_start_end = []
    for start_end in random_start_end(start_end_len, start_date):
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
