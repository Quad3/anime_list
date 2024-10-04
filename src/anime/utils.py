import uuid
from datetime import date

from fastapi import HTTPException, status

from .models import AnimeStartEnd


def is_start_end_valid(start_date: date, end_date: date):
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="End date can't be earlier than start date",
        )
    return True


def fill_start_end(
        source: list[dict[str, date]],
        anime_id: uuid.UUID,
) -> list[AnimeStartEnd]:
    destination: list[AnimeStartEnd] = []
    for start_end in source:
        start_date = start_end.get("start_date")
        end_date = start_end.get("end_date")
        if start_date and end_date:
            is_start_end_valid(start_date, end_date)

        destination.append(AnimeStartEnd(
            start_date=start_date,
            end_date=end_date,
            anime_id=anime_id),
        )
    return destination
