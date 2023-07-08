from typing import Any

from httpx import AsyncClient
from jose import jwt
import pytest

from auth.utils import decode_token


@pytest.mark.asyncio
async def test_login(migrate_db: Any, async_client: AsyncClient, admin_user: Any) -> None:
    data = {'email': 'admin@admin.net', 'password': '123456'}
    response = await async_client.post('/auth/login', json=data)
    assert response.status_code == 200
    result = response.json()
    assert 'access_token' in result

    access_token = result['access_token']

    claims = jwt.get_unverified_claims(access_token)
    assert claims['sub'] == 'admin@admin.net'
    assert claims['profile']['first_name'] == 'Admin'
    assert claims['profile']['is_admin'] is True

    claims = decode_token(access_token)
    assert claims['sub'] == 'admin@admin.net'
    assert claims['profile']['first_name'] == 'Admin'
    assert claims['profile']['is_admin'] is True
