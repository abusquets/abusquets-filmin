from typing import Any

from faker import Faker
from httpx import AsyncClient
import pytest


fake = Faker()


@pytest.mark.asyncio
async def test_production_company_create(
    async_admin_client: AsyncClient,
    clean_production_company: Any,  # noqa: ARG001
) -> None:
    data = {'name': fake.company()}
    response = await async_admin_client.post('/filmin/production-company', json=data)
    assert response.status_code == 201
    result = response.json()
    assert 'uuid' in result


@pytest.mark.asyncio
async def test_production_company_list(
    async_normal_client: AsyncClient,
    production_company1: dict[str, str],
    production_company2: dict[str, str],
) -> None:
    uuids = [production_company1['uuid'], production_company2['uuid']]
    names = [production_company1['name'], production_company2['name']]
    response = await async_normal_client.get('/filmin/production-company')
    assert response.status_code == 200
    paginated_result = response.json()
    assert 'results' in paginated_result
    assert len(paginated_result['results']) == 2
    for result in paginated_result['results']:
        assert 'uuid' in result and result['uuid'] in uuids
        assert 'name' in result and result['name'] in names


@pytest.mark.asyncio
async def test_production_company_detail(async_normal_client: AsyncClient, production_company1: dict[str, str]) -> None:
    response = await async_normal_client.get(f"/filmin/production-company/{production_company1['uuid']}")
    assert response.status_code == 200
    result = response.json()
    assert 'name' in result and result['name'] == production_company1['name']


@pytest.mark.asyncio
async def test_production_company_update(async_admin_client: AsyncClient, production_company1: dict[str, str]) -> None:
    data = {'name': fake.company()}
    response = await async_admin_client.put(f"/filmin/production-company/{production_company1['uuid']}", json=data)
    assert response.status_code == 200
    result = response.json()
    assert 'name' in result
    assert result['name'] == data['name']


@pytest.mark.asyncio
async def test_production_company_update_partial(
    async_admin_client: AsyncClient, production_company1: dict[str, str]
) -> None:
    data = {'name': fake.company()}
    response = await async_admin_client.patch(f"/filmin/production-company/{production_company1['uuid']}", json=data)
    assert response.status_code == 200
    result = response.json()
    assert 'name' in result
    assert result['name'] == data['name']
