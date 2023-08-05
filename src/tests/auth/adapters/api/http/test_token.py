from httpx import AsyncClient
import pytest

from auth.domain.services.token import TokenService


@pytest.mark.asyncio
async def test_use_refresh_token_error(async_client: AsyncClient, token_service: TokenService) -> None:
    refresh_token = token_service.create_refresh_token(
        'admin@admin.poc', {'profile': {'first_name': 'Admin', 'is_admin': True}}
    )
    async_client.headers.update({'Authorization': f'Bearer {refresh_token}'})
    response = await async_client.get('/auth/protected')
    assert response.status_code == 401
    result = response.json()
    assert result['detail'] == 'Invalid token.'


@pytest.mark.asyncio
async def test_expired_token(async_client: AsyncClient) -> None:
    access_token = TokenService._create_token(  # noqa: SLF001
        'a', 'admin@admin.poc', {'profile': {'first_name': 'Admin', 'is_admin': True}}, -1
    )
    async_client.headers.update({'Authorization': f'Bearer {access_token}'})
    response = await async_client.get('/auth/protected')
    assert response.status_code == 401
    result = response.json()
    assert result['detail'] == 'Invalid token or expired token.'


@pytest.mark.asyncio
async def test_refresh_token(async_client: AsyncClient, token_service: TokenService) -> None:
    refresh_token = token_service.create_refresh_token(
        'admin@admin.poc', {'profile': {'first_name': 'Admin', 'is_admin': True}}
    )
    async_client.headers.update({'Authorization': f'Bearer {refresh_token}'})
    response = await async_client.post('/auth/refresh-token')
    assert response.status_code == 200
    access_token = response.json()['access_token']
    claims = token_service.decode_token(access_token)
    assert claims is not None
    assert claims['sub'] == 'admin@admin.poc'
    assert claims['profile']['first_name'] == 'Admin'
    assert claims['profile']['is_admin'] is True


@pytest.mark.asyncio
async def test_refresh_token_with_access_error(async_client: AsyncClient, token_service: TokenService) -> None:
    refresh_token = token_service.create_access_token(
        'admin@admin.poc', {'profile': {'first_name': 'Admin', 'is_admin': True}}
    )
    async_client.headers.update({'Authorization': f'Bearer {refresh_token}'})
    response = await async_client.post('/auth/refresh-token')
    assert response.status_code == 401
