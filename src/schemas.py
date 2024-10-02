from pydantic import BaseModel
from typing import List

class RecipeBase(BaseModel):
    title: str
    description: str | None = None
    prep_time: int | None = None
    cook_time: int | None = None
    servings: int | None = 1

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    author_id: int
    rating: float = 0.0

    class Config:
        orm_mode = True



class MealplanBase(BaseModel):
    title: str

class Mealplan(MealplanBase):
    id: int
    author_id: int
    meals: str

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    user_id: int | None = None

class Ingredient(BaseModel):
    id: int
    name: str

class MacroBase(BaseModel):
    calories: int | None = None
    protein: int | None = None
    carbohydrates: int | None = None
    fats: int | None = None

class MacroCreate(MacroBase):
    pass

class Macro(MacroBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True

class Tag(BaseModel):
    id: int
    tag: str

class RecipeResponse(BaseModel):
    recipe: Recipe
    quantities: List[object]
    macros: List[MacroBase]
    instructions: List[str]
    tags: List[Tag]
    meals: List[object]