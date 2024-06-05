from pydantic import BaseModel


class RecipeBase(BaseModel):
    title: str
    description: str | None = None


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    recipes: list[Recipe] = []

    class Config:
        orm_mode = True