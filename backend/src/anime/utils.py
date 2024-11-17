from datetime import date

from fastapi import HTTPException, status

from .models import AnimeStartEnd, State
from .schemas import StartEndCreate


def fill_start_end_if_valid(source: list[StartEndCreate] | None) -> list[AnimeStartEnd]:
    if source is None:
        return []

    destination: list[AnimeStartEnd] = []
    for start_end in source:
        start_date = start_end.get("start_date")
        end_date = start_end.get("end_date")
        if start_date and end_date:
            is_start_end_valid_or_raise(start_date, end_date)

        destination.append(AnimeStartEnd(
            start_date=start_date,
            end_date=end_date,
        ))
    return destination


def is_start_end_valid_or_raise(start_date: date, end_date: date) -> bool:
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="End date can't be earlier than start date",
        )
    return True


def determine_anime_state(start_end_list: list[StartEndCreate] | None) -> State:
    if not start_end_list:
        return State.PLAN_TO_WATCH
    if not start_end_list[-1].get("end_date", None):
        return State.WATCHING
    else:
        return State.WATCHED
