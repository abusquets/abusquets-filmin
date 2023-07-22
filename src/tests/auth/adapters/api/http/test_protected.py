from httpx import AsyncClient
import pytest

from auth.domain.services.token import TokenService


@pytest.mark.asyncio
async def test_protected(async_client: AsyncClient, token_service: TokenService) -> None:
    access_token = token_service.create_access_token(
        'admin@admin.poc', {'profile': {'first_name': 'Admin', 'is_admin': True}}
    )
    async_client.headers.update({'Authorization': f'Bearer {access_token}'})
    response = await async_client.get('/auth/protected')
    assert response.status_code == 200
    result = response.json()
    assert 'username' in result

    assert result['username'] == 'admin@admin.poc'
