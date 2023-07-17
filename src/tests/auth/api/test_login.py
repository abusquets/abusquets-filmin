from httpx import AsyncClient
import pytest

from auth.utils import decode_token
from core.domain.schemas.user import User


@pytest.mark.asyncio
async def test_login(async_client: AsyncClient, admin_user: User) -> None:
    data = {'email': admin_user.email, 'password': '123456'}
    response = await async_client.post('/auth/login', json=data)
    assert response.status_code == 200
    result = response.json()
    assert 'access_token' in result

    access_token = result['access_token']

    claims = decode_token(access_token)
    assert claims
    assert claims['sub'] == admin_user.email
    assert claims['profile']['first_name'] == admin_user.first_name
    assert claims['profile']['is_admin'] == admin_user.is_admin
