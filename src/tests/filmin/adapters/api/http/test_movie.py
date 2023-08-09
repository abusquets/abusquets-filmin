from typing import Any

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_movie_create(
    clean_movie: Any,  # noqa: ARG001
    async_admin_client: AsyncClient,
    genre_comedy: Any,  # noqa: ARG001
    genre_animation: Any,  # noqa: ARG001
    collection_toy_story: str,
) -> None:
    data = {
        'title': 'Toy Story',
        'release_date': '1995-10-30',
        'budget': 30000000,
        'revenue': 373554033,
        # 'popularity': 21.946943,
        'collection': collection_toy_story,
        'genres': ['animation', 'comedy'],
        'original_language': 'en',
        'overview': (
            "Led by Woody, Andy's toys live happily in his room until "
            "Andy's birthday brings Buzz Lightyear onto the scene. "
            "Afraid of losing his place in Andy's heart, Woody plots against Buzz. "
            'But when circumstances separate Buzz and Woody from their owner, '
            'the duo eventually learns to put aside their differences.'
        ),
    }
    response = await async_admin_client.post('/filmin/movie', json=data)
    assert response.status_code == 201
    result = response.json()
    assert 'uuid' in result


@pytest.mark.asyncio
async def test_movie_detail(
    clean_movie: Any, async_client: AsyncClient, movie_toy_story2: Any, collection_toy_story: str  # noqa: ARG001
) -> None:
    response = await async_client.get(f'/filmin/movie/{movie_toy_story2}')
    assert response.status_code == 200
    result = response.json()
    assert 'uuid' in result and result['uuid'] == movie_toy_story2
    assert 'release_date' in result and result['release_date'] == '2000-10-30'
    assert 'collection' in result and result['collection']['uuid'] == collection_toy_story
    assert 'original_language' in result and result['original_language'] == 'en'
    assert 'overview' in result and result['overview'] == 'Test overview'
    assert 'genres' in result
    assert len(result['genres']) == 2
    genres = [genre['code'] for genre in result['genres']]
    assert 'animation' in genres
    assert 'comedy' in genres


@pytest.mark.asyncio
async def test_movie_list(
    clean_movie: Any, async_client: AsyncClient, collection_toy_story: str, movie_toy_story2: str  # noqa: ARG001
) -> None:
    response = await async_client.get('/filmin/movie')
    assert response.status_code == 200
    paginated_result = response.json()
    assert 'results' in paginated_result
    assert len(paginated_result['results']) == 1
    result = paginated_result['results'][0]
    assert 'uuid' in result and result['uuid'] == movie_toy_story2
    assert 'release_date' in result and result['release_date'] == '2000-10-30'
    assert 'collection' in result and result['collection']['uuid'] == collection_toy_story
    assert 'original_language' in result and result['original_language'] == 'en'
    assert 'overview' in result and result['overview'] == 'Test overview'
    assert 'genres' in result
    assert len(result['genres']) == 2
    genres = [genre['code'] for genre in result['genres']]
    assert 'animation' in genres
    assert 'comedy' in genres


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'attribute, value',
    [
        (
            'title',
            'Toy Story - wip',
        ),
        (
            'release_date',
            '1995-10-31',
        ),
    ],
)
async def test_movie_update_partial(
    clean_movie: Any,  # noqa: ARG001
    async_admin_client: AsyncClient,
    movie_toy_story2: Any,
    collection_fake: str,  # noqa: ARG001
    attribute: str,
    value: str,
) -> None:
    data = {
        attribute: value,
    }
    response = await async_admin_client.patch(f'/filmin/movie/{movie_toy_story2}', json=data)
    assert response.status_code == 200

    result = response.json()
    assert result[attribute] == value


@pytest.mark.asyncio
async def test_movie_update_partial_collection(
    clean_movie: Any, async_admin_client: AsyncClient, movie_toy_story2: Any, collection_fake: str  # noqa: ARG001
) -> None:
    data = {'collection': collection_fake}
    response = await async_admin_client.patch(f'/filmin/movie/{movie_toy_story2}', json=data)
    assert response.status_code == 200

    result = response.json()
    assert 'collection' in result and result['collection']['uuid'] == collection_fake


@pytest.mark.asyncio
async def test_movie_update_genres(
    clean_movie: Any, async_admin_client: AsyncClient, movie_toy_story2: Any, genre_fake: str  # noqa: ARG001
) -> None:
    data = {'genres': ['animation', 'fake-genre']}
    response = await async_admin_client.patch(f'/filmin/movie/{movie_toy_story2}', json=data)
    assert response.status_code == 200

    result = response.json()
    assert [genre['code'] for genre in result['genres']] == ['animation', 'fake-genre']
