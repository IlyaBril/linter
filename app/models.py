from sqlalchemy import Column, Integer, String

from .database import Base


class BaseRecipe(Base):
    """
    Represents a recipe base class.

    Attributes:
        id (int): The primary key of the recipe.
        dish_name (str): The name of the dish
        preparation_time (int): Preparation time of the dish in minutes.
    """

    __tablename__ = "Recipe"

    id = Column(Integer, primary_key=True, index=True)
    dish_name = Column(String, index=True)
    preparation_time = Column(Integer, index=True)


class RecipeList(BaseRecipe):
    """
    Represents class used for return list of recipes (dishes).

    Attributes:
        view_count (int): number representing quantity of views
    """

    view_count = Column(Integer, index=True, default=0)


class Recipe(BaseRecipe):
    """
    Represents class used for return recipe by id or
    to add a new recipe to the database.

    Attributes:
        product_list (str): list of ingredients necessary for dish preparation
        recipe_description(str): recipe description
    """

    product_list = Column(String, index=True)
    recipe_description = Column(String, index=True)
