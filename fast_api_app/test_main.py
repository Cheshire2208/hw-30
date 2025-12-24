import pytest
from httpx import AsyncClient, ASGITransport
import models
from main import app, get_db
from database import async_session


@pytest.fixture(scope="function")
async def client():
    async def override_get_db():
        async with async_session() as db_session:
            yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with async_session().bind.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac

    async with async_session().bind.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_recipe(client):
    response = await client.post('/recipes/', json={
        "recipe_name": "test",
        "cooking_time_minutes": 10,
        "ingredients": "smth1, smth2",
        "description": "for testing"
    })
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_all_recipes(client):
    response = await client.get('/recipes/' )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_recipe_details(client):
    response = await client.post('/recipes/', json={
        "recipe_name": "test",
        "cooking_time_minutes": 10,
        "ingredients": "smth1, smth2",
        "description": "for testing"
    })
    recipe_id = response.json()['id']
    response = await client.get(f'/recipes/{recipe_id}' )
    assert response.status_code == 200
