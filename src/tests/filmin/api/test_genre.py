from typing import Any

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_genre_create(migrate_db: Any, async_client: AsyncClient) -> None:
    data = {'code': 'melodrama', 'name': 'Melodrama'}
    response = await async_client.post('/filmin/genre', json=data)
    assert response.status_code == 201
    result = response.json()
    assert 'code' in result and result['code'] == 'melodrama'


@pytest.mark.asyncio
async def test_genre_list(migrate_db: Any, async_client: AsyncClient, genre_western: str) -> None:
    response = await async_client.get('/filmin/genre')
    assert response.status_code == 200
    paginated_result = response.json()
    assert 'results' in paginated_result
    codes = [item.get('code') for item in paginated_result['results']]
    assert 'western' in codes


@pytest.mark.asyncio
async def test_genre_detail(migrate_db: Any, async_client: AsyncClient, genre_western: str) -> None:
    response = await async_client.get(f'/filmin/genre/{genre_western}')
    assert response.status_code == 200
    result = response.json()
    assert 'code' in result and result['code'] == 'western'


@pytest.mark.asyncio
async def test_genre_update(migrate_db: Any, async_client: AsyncClient, genre_western: str) -> None:
    data = {'name': 'Western - wip'}
    response = await async_client.put(f'/filmin/genre/{genre_western}', json=data)
    assert response.status_code == 200
    result = response.json()
    assert 'name' in result
    assert result['name'] == 'Western - wip'


@pytest.mark.asyncio
async def test_genre_update_partial(migrate_db: Any, async_client: AsyncClient, genre_western: str) -> None:
    data = {'name': 'Western - example'}
    response = await async_client.patch(f'/filmin/genre/{genre_western}', json=data)
    assert response.status_code == 200
    result = response.json()
    assert 'name' in result
    assert result['name'] == 'Western - example'
