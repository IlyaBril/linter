from pydantic import BaseModel


class BaseRecipe(BaseModel):
    dish_name: str
    preparation_time: int


class RecipeListOut(BaseRecipe):
    view_count: int | None

    class Config:
        orm_mode = True


class RecipeInOut(BaseRecipe):
    id: int
    product_list: str
    recipe_description: str

    class Config:
        orm_mode = True


class RecipeIn(BaseRecipe):
    product_list: str
    recipe_description: str
