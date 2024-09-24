import random
import string
from datetime import date, timedelta
from typing import Any


def random_lower_string(k: int = 16) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))


def random_start_end(k: int = 1) -> list[dict[date | Any]]:
    res = []
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
