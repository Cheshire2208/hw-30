from typing import AsyncGenerator, List

import models
import schemas
from database import async_session, engine, session
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


get_db_dep = Depends(get_db)


@app.post(
    "/recipes/",
    response_model=schemas.RecipeDetailOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_recipe(recipe: schemas.RecipeCreate, db: AsyncSession = get_db_dep):
    stmt = select(models.Recipe).where(models.Recipe.recipe_name == recipe.recipe_name)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400, detail="Рецепт с таким названием уже существует"
        )

    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe


@app.get("/recipes/", response_model=List[schemas.RecipeListOut])
async def get_recipes_list(
    skip: int = 0, limit: int = 100, db: AsyncSession = get_db_dep
):
    stmt = (
        select(models.Recipe)
        .order_by(desc(models.Recipe.views_count), models.Recipe.cooking_time_minutes)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeDetailOut)
async def get_recipe_detail(recipe_id: int, db: AsyncSession = get_db_dep):
    stmt = select(models.Recipe).where(models.Recipe.id == recipe_id)
    result = await db.execute(stmt)
    recipe = result.scalar_one_or_none()

    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    recipe.views_count = int(recipe.views_count + 1)
    await db.commit()

    return recipe
