from pydantic import BaseModel

class RecipeBase(BaseModel):
    title: str
    description: str | None = None
    prep_time: int | None = None
    cook_time: int | None = None

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    author_id: int
    rating: float = 0.0

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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    user_id: int | None = None

