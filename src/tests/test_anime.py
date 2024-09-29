import uuid
from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from anime.models import State
from anime.router import router
from .utils.anime import create_random_anime
from .utils.utils import user_token_headers
from auth.deps import get_current_user


ANIME_PREFIX = router.prefix


@pytest.fixture()
def anime_in() -> dict[str, str | list[dict[str, str] | dict[str, str]] | int]:
    return {
        "name": "Naruto",
        "rate": 10,
        "state": State.WATCHED,
        "review": "Top",
        "start_end": [
            {
                "start_date": "2020-01-01",
                "end_date": "2020-03-03"
            }
        ]
    }


@pytest.mark.anyio
async def test_get_anime_list_empty(async_client: AsyncClient, test_db: AsyncSession):
    response = await async_client.get(f"{ANIME_PREFIX}/")
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "There is no anime yet"


@pytest.mark.anyio
async def test_get_anime_list_page_out_of_range(async_client: AsyncClient, test_db: AsyncSession):
    await create_random_anime(test_db)
    await create_random_anime(test_db)
    response = await async_client.get(f"{ANIME_PREFIX}/", params={"limit": 1, "page": 3})
    assert response.status_code == 404
    assert response.json()["detail"] == "Out-of-Range page request"


@pytest.mark.anyio
async def test_create_anime_fail(
        async_client: AsyncClient,
        test_db: AsyncSession,
        anime_in: dict,
):
    anime_in["start_end"].append({
        "start_date": "2024-02-02",
        "end_date": "2024-01-01"
    })
    headers = await user_token_headers(async_client, test_db)
    response = await async_client.post(
        f"{ANIME_PREFIX}/create",
        json=anime_in,
        headers=headers,
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "End date can't be earlier than start date"
    anime_list_response = await async_client.get(f"{ANIME_PREFIX}/")
    assert anime_list_response.status_code == 404
    assert anime_list_response.json()["detail"] == "There is no anime yet"


@pytest.mark.anyio
async def test_create_anime(
        async_client: AsyncClient,
        test_db: AsyncSession,
        anime_in: dict,
):
    headers = await user_token_headers(async_client, test_db)
    user = await get_current_user(test_db, headers["Authorization"].split()[1])
    response = await async_client.post(
        f"{ANIME_PREFIX}/create",
        json=anime_in,
        headers=headers,
    )
    assert response.status_code == 201
    created_anime = response.json()
    assert created_anime.items() >= anime_in.items()
    assert created_anime["user_id"] == str(user.uuid)
    assert "uuid" in created_anime


@pytest.mark.anyio
async def test_get_one_anime(async_client: AsyncClient, test_db: AsyncSession):
    anime = await create_random_anime(test_db, start_end_len=3)
    response = await async_client.get(f"{ANIME_PREFIX}/{anime.uuid}")
    assert response.status_code == 200
    anime_response = response.json()
    assert anime_response["name"] == anime.name
    assert anime_response["rate"] == anime.rate
    assert anime_response["state"] == anime.state
    assert anime_response["review"] == anime.review
    for response_start_end, anime_start_end in zip(anime_response["start_end"], anime.start_end):
        assert response_start_end["start_date"] == str(anime_start_end.start_date)
        assert response_start_end["end_date"] == str(anime_start_end.end_date)
    assert anime_response["uuid"] == str(anime.uuid)


@pytest.mark.anyio
async def test_get_one_anime_not_found(async_client: AsyncClient, test_db: AsyncSession):
    response = await async_client.get(f"{ANIME_PREFIX}/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Anime with this id does not exist"


@pytest.mark.anyio
async def test_update_anime(async_client: AsyncClient, test_db: AsyncSession):
    anime = await create_random_anime(test_db, start_end_len=2)
    data = {"name": "Updated name", "review": "Updated review"}
    response = await async_client.patch(f"{ANIME_PREFIX}/{anime.uuid}/update", json=data)
    assert response.status_code == 200
    anime_response = response.json()
    assert anime_response["name"] == data["name"]
    assert anime_response["rate"] == anime.rate
    assert anime_response["state"] == anime.state
    assert anime_response["review"] == data["review"]
    assert "uuid" not in anime_response


@pytest.mark.anyio
async def test_update_anime_not_found(async_client: AsyncClient, test_db: AsyncSession):
    data = {"name": "Updated name", "review": "Updated review"}
    response = await async_client.patch(f"{ANIME_PREFIX}/{str(uuid.uuid4())}/update", json=data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Anime with this id does not exist"


@pytest.mark.anyio
async def test_create_anime_start_end(async_client: AsyncClient, test_db: AsyncSession):
    anime = await create_random_anime(test_db, start_end_len=1)
    data = {"start_date": "2030-01-01"}
    response = await async_client.post(f"{ANIME_PREFIX}/{anime.uuid}/create-start-end", json=data)
    assert response.status_code == 201
    start_end_response = response.json()
    assert len(start_end_response) == 2
    assert start_end_response["start_date"] == data["start_date"]
    assert start_end_response["end_date"] is None


@pytest.mark.anyio
async def test_create_anime_start_end_fail(async_client: AsyncClient, test_db: AsyncSession):
    anime = await create_random_anime(test_db, start_end_len=1)
    data = {"start_date": "2030-01-01", "end_date": "2029-12-12"}
    response = await async_client.post(f"{ANIME_PREFIX}/{anime.uuid}/create-start-end", json=data)
    assert response.status_code == 409
    assert response.json()["detail"] == "End date can't be earlier than start date"


@pytest.mark.anyio
async def test_update_anime_start_end(async_client: AsyncClient, test_db: AsyncSession):
    anime = await create_random_anime(test_db, start_end_len=3)
    data = {"end_date": "2030-01-01"}
    response = await async_client.patch(f"{ANIME_PREFIX}/{anime.uuid}/update-start-end", json=data)
    assert response.status_code == 200
    start_end_response = response.json()
    assert start_end_response["end_date"] == data["end_date"]


@pytest.mark.anyio
async def test_update_anime_start_end_not_found(async_client: AsyncClient, test_db: AsyncSession):
    data = {"end_date": "2000-01-01"}
    response = await async_client.patch(f"{ANIME_PREFIX}/{str(uuid.uuid4())}/update-start-end", json=data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Data not found"


@pytest.mark.anyio
async def test_update_anime_start_end_fail(async_client: AsyncClient, test_db: AsyncSession):
    anime = await create_random_anime(test_db, start_end_len=2)
    data = {"end_date": "2000-01-01"}
    response = await async_client.patch(f"{ANIME_PREFIX}/{anime.uuid}/update-start-end", json=data)
    assert response.status_code == 409
    assert response.json()["detail"] == "End date can't be earlier than start date"
