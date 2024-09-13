from datetime import date

from fastapi import HTTPException, status


def is_start_end_valid(start_date: date, end_date: date):
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="End date can't be earlier than start date"
        )
    return True
