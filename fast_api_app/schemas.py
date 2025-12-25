from pydantic import BaseModel


class RecipeCreate(BaseModel):
    recipe_name: str
    cooking_time_minutes: int
    ingredients: str
    description: str


class RecipeListOut(BaseModel):
    id: int
    recipe_name: str
    views_count: int
    cooking_time_minutes: int

    class Config:
        from_attributes = True


class RecipeDetailOut(BaseModel):
    id: int
    recipe_name: str
    views_count: int
    cooking_time_minutes: int
    ingredients: str
    description: str

    class Config:
        from_attributes = True
