import logging
from typing import List, Optional, Dict

from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select

from ..app import models, schemas
from ..app.database import engine, session

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    # await asyncio.shield
    await engine.dispose()


@app.post("/recipes/", response_model=schemas.RecipeIn)
async def recipes(recipe: schemas.RecipeIn) -> models.Recipe:
    """
    Endpoint to add a new recipe to the database.
    Args:
        recipe (Recipe): Recipe data provided in the request body.
    Returns:
        models.Recipe: A message indicating the success of the operation.
    """
    new_recipe = models.Recipe(**recipe.dict())
    # async with session.begin():
    session.add(new_recipe)
    await session.commit()
    return new_recipe


@app.get("/recipes/{idx}", response_model=schemas.RecipeInOut)
@app.get("/recipes/", response_model=List[schemas.RecipeListOut])
async def recipes_idx(idx: Optional[int] = None) -> List[Dict | None]:
    """
    Endpoint to retrieve a list of all or single recipe if idx provided.
    Returns:
        List[RecipeList]:
        list of RecipeList objects representing all recipes in the database.
        or, if idx provided:
        RecipeList:
        recipe returned by id number. Increase view_count by 1

    """
    if idx:
        recipe = await session.get(models.Recipe, idx)
        count = await session.get(models.RecipeList, idx)
        if not recipe or not count:
            raise HTTPException(status_code=404, detail="Recipe not found")

        count.view_count = count.view_count + 1

        await session.commit()
    else:
        recipe = await session.execute(
            select(models.RecipeList).order_by(
                models.RecipeList.view_count.desc(),
                models.RecipeList.preparation_time.desc(),
            )
        )
        recip = recipe.scalars().all()
    return recip
