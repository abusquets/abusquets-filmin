from typing import Any

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_country_list(async_client: AsyncClient, country_spain: Any) -> None:  # noqa: ARG001
    response = await async_client.get('/core/country')
    assert response.status_code == 200
    result = response.json()
    codes = [item.get('code') for item in result]
    assert 'ES' in codes


@pytest.mark.asyncio
async def test_country_detail(async_client: AsyncClient, country_spain: Any) -> None:  # noqa: ARG001
    response = await async_client.get('/core/country/ES')
    assert response.status_code == 200
    result = response.json()
    assert 'code' in result and result['code'] == 'ES'
