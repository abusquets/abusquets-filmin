from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_hello_world(async_client: AsyncClient) -> None:
    response = await async_client.get('/')
    assert response.status_code == 200

    data = response.json()
    assert data['message'] == 'Hello World'
