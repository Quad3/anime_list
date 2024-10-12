import uuid
from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from anime.models import State
from anime.router import router
from .utils.anime import create_random_anime
from .utils.utils import user_token_headers
from .utils.auth import create_random_user
from auth.deps import get_current_user


ANIME_PREFIX = router.prefix


@pytest.fixture()
def anime_in() -> dict[str, str | list[dict[str, str] | dict[str, str]] | int]:
    return {
        "name": "Naruto",
        "rate": 10,
        "review": "Top",
        "start_end": [
            {
                "start_date": "2020-01-01",
                "end_date": "2020-03-03"
            },
            {
                "start_date": "2021-02-02",
                "end_date": "2021-02-12"
            },
        ]
    }


@pytest.mark.anyio
async def test_get_anime_list_empty(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    response = await async_client.get(
        f"{ANIME_PREFIX}",
        headers=headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "There is no anime yet"


@pytest.mark.anyio
async def test_get_anime_list_page_out_of_range(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await get_current_user(test_db, headers["Authorization"].split()[1])
    await create_random_anime(test_db, user_id=user.uuid)
    await create_random_anime(test_db, user_id=user.uuid)
    response = await async_client.get(
        f"{ANIME_PREFIX}",
        params={"limit": 1, "page": 3},
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Out-of-Range page request"


@pytest.mark.anyio
async def test_get_anime_list(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await get_current_user(test_db, headers["Authorization"].split()[1])
    anime1 = await create_random_anime(
        test_db,
        start_date=date(year=2010, month=1, day=1),
        user_id=user.uuid,
    )
    anime2 = await create_random_anime(
        test_db,
        start_date=date(year=2014, month=1, day=1),
        start_end_len=2,
        user_id=user.uuid,
    )
    response = await async_client.get(
        f"{ANIME_PREFIX}",
        params={"limit": 5, "page": 1},
        headers=headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["count"] != 0
    for cont, anime in zip(content["data"], [anime1, anime2]):
        assert cont["uuid"] == str(anime.uuid)
        assert cont["name"] == anime.name
        assert cont["rate"] == anime.rate
        assert cont["review"] == anime.review
        assert cont["state"] == anime.state
        for content_start_end, anime_start_end in zip(cont["start_end"], anime.start_end):
            assert content_start_end["start_date"] == str(anime_start_end.start_date)
            assert content_start_end["end_date"] == str(anime_start_end.end_date)


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
    anime_list_response = await async_client.get(
        f"{ANIME_PREFIX}",
        headers=headers,
    )
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
async def test_create_anime_state_plan_to_watch(
        async_client: AsyncClient,
        test_db: AsyncSession,
        anime_in: dict,
):
    anime_in_without_start_end = anime_in.copy()
    anime_in_without_start_end.pop("start_end")
    headers = await user_token_headers(async_client, test_db)
    response = await async_client.post(
        f"{ANIME_PREFIX}/create",
        json=anime_in_without_start_end,
        headers=headers,
    )
    assert response.status_code == 201
    created_anime = response.json()
    assert created_anime["state"] == State.PLAN_TO_WATCH


@pytest.mark.anyio
async def test_create_anime_state_watched(
        async_client: AsyncClient,
        test_db: AsyncSession,
        anime_in: dict,
):
    headers = await user_token_headers(async_client, test_db)
    response = await async_client.post(
        f"{ANIME_PREFIX}/create",
        json=anime_in,
        headers=headers,
    )
    assert response.status_code == 201
    created_anime = response.json()
    assert created_anime["state"] == State.WATCHED


@pytest.mark.anyio
async def test_create_anime_state_watching(
        async_client: AsyncClient,
        test_db: AsyncSession,
        anime_in: dict,
):
    anime_in["start_end"].append({"start_date": "2024-02-02"})
    headers = await user_token_headers(async_client, test_db)
    response = await async_client.post(
        f"{ANIME_PREFIX}/create",
        json=anime_in,
        headers=headers,
    )
    assert response.status_code == 201
    created_anime = response.json()
    assert created_anime["state"] == State.WATCHING


@pytest.mark.anyio
async def test_get_one_anime(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await get_current_user(test_db, headers["Authorization"].split()[1])
    anime = await create_random_anime(test_db, start_end_len=3, user_id=user.uuid)
    response = await async_client.get(
        f"{ANIME_PREFIX}/{anime.uuid}",
        headers=headers,
    )
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
    assert anime_response["user_id"] == str(user.uuid)


@pytest.mark.anyio
async def test_get_one_anime_not_found(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    response = await async_client.get(
        f"{ANIME_PREFIX}/{str(uuid.uuid4())}",
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Anime with this id does not exist"


@pytest.mark.anyio
async def test_update_anime(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await get_current_user(test_db, headers["Authorization"].split()[1])
    anime = await create_random_anime(test_db, start_end_len=2, user_id=user.uuid)
    data = {"name": "Updated name", "review": "Updated review"}
    response = await async_client.patch(
        f"{ANIME_PREFIX}/{anime.uuid}/update",
        json=data,
        headers=headers,
    )
    assert response.status_code == 200
    anime_response = response.json()
    assert anime_response["name"] == data["name"]
    assert anime_response["rate"] == anime.rate
    assert anime_response["state"] == anime.state
    assert anime_response["review"] == data["review"]
    assert "uuid" not in anime_response


@pytest.mark.anyio
async def test_update_anime_not_found(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    data = {"name": "Updated name", "review": "Updated review"}
    response = await async_client.patch(
        f"{ANIME_PREFIX}/{str(uuid.uuid4())}/update",
        json=data,
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Anime with this id does not exist"


@pytest.mark.anyio
async def test_create_anime_start_end(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await get_current_user(test_db, headers["Authorization"].split()[1])
    anime = await create_random_anime(test_db, start_end_len=1, user_id=user.uuid)
    data = {"start_date": "2030-01-01"}
    response = await async_client.post(
        f"{ANIME_PREFIX}/{anime.uuid}/create-start-end",
        json=data,
        headers=headers,
    )
    assert response.status_code == 201
    start_end_response = response.json()
    assert len(start_end_response) == 2
    assert start_end_response["start_date"] == data["start_date"]
    assert start_end_response["end_date"] is None


@pytest.mark.anyio
async def test_create_anime_start_end_fail(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await get_current_user(test_db, headers["Authorization"].split()[1])
    anime = await create_random_anime(test_db, start_end_len=1, user_id=user.uuid)
    data = {"start_date": "2030-01-01", "end_date": "2029-12-12"}
    response = await async_client.post(
        f"{ANIME_PREFIX}/{anime.uuid}/create-start-end",
        json=data,
        headers=headers,
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "End date can't be earlier than start date"


@pytest.mark.anyio
async def test_create_anime_start_end_not_enough_permissions(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await create_random_user(test_db)
    anime = await create_random_anime(test_db, start_end_len=1, user_id=user.uuid)
    data = {"start_date": "2030-01-01", "end_date": "2030-12-12"}
    response = await async_client.post(
        f"{ANIME_PREFIX}/{anime.uuid}/create-start-end",
        json=data,
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough permissions"


@pytest.mark.anyio
async def test_create_anime_start_end_not_found(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    data = {"start_date": "2030-01-01", "end_date": "2030-12-12"}
    response = await async_client.post(
        f"{ANIME_PREFIX}/{uuid.uuid4()}/create-start-end",
        json=data,
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Anime with this id does not exist"


@pytest.mark.anyio
async def test_update_anime_start_end(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await get_current_user(test_db, headers["Authorization"].split()[1])
    anime = await create_random_anime(test_db, start_end_len=3, user_id=user.uuid)
    data = {"end_date": "2030-01-01"}
    response = await async_client.patch(
        f"{ANIME_PREFIX}/{anime.uuid}/update-start-end",
        json=data,
        headers=headers,
    )
    assert response.status_code == 200
    start_end_response = response.json()
    assert start_end_response["end_date"] == data["end_date"]


@pytest.mark.anyio
async def test_update_anime_start_end_data_not_found(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await get_current_user(test_db, headers["Authorization"].split()[1])
    anime = await create_random_anime(test_db, start_end_len=0, user_id=user.uuid)
    data = {"end_date": "2000-01-01"}
    response = await async_client.patch(
        f"{ANIME_PREFIX}/{anime.uuid}/update-start-end",
        json=data,
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Data not found"


@pytest.mark.anyio
async def test_update_anime_start_end_anime_not_found(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    data = {"end_date": "2000-01-01"}
    response = await async_client.patch(
        f"{ANIME_PREFIX}/{str(uuid.uuid4())}/update-start-end",
        json=data,
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Anime with this id does not exist"


@pytest.mark.anyio
async def test_update_anime_start_end_fail(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await get_current_user(test_db, headers["Authorization"].split()[1])
    anime = await create_random_anime(test_db, start_end_len=2, user_id=user.uuid)
    data = {"end_date": "2000-01-01"}
    response = await async_client.patch(
        f"{ANIME_PREFIX}/{anime.uuid}/update-start-end",
        json=data,
        headers=headers,
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "End date can't be earlier than start date"


@pytest.mark.anyio
async def test_update_anime_start_end_not_enough_permissions(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await create_random_user(test_db)
    anime = await create_random_anime(test_db, start_end_len=2, user_id=user.uuid)
    data = {"end_date": "2000-01-01"}
    response = await async_client.patch(
        f"{ANIME_PREFIX}/{anime.uuid}/update-start-end",
        json=data,
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough permissions"


@pytest.mark.anyio
async def test_get_anime_start_end_list(async_client: AsyncClient, test_db: AsyncSession):
    headers = await user_token_headers(async_client, test_db)
    user = await get_current_user(test_db, headers["Authorization"].split()[1])
    anime1 = await create_random_anime(test_db, start_end_len=2, user_id=user.uuid)
    anime2 = await create_random_anime(test_db, start_end_len=3, user_id=user.uuid)
    response = await async_client.get(
        f"{ANIME_PREFIX}/start-end-list",
        headers=headers,
    )
    content = response.json()
    assert len(content) == 5
    assert sum([str(anime1.uuid) == start_end['anime_id'] for start_end in content]) == 2
    assert sum([str(anime2.uuid) == start_end['anime_id'] for start_end in content]) == 3
