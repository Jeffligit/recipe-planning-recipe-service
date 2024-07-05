from .database import Base

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    recipes = relationship("Recipe", back_populates="author")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    prep_time = Column(Integer)
    cook_time = Column(Integer)
    rating = Column(Float(2))
    author = relationship("User", back_populates="recipes")
    macros = relationship("Macro", back_populates="recipe")

class Ingredient(Base):
    __tablename__= "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

class Macro(Base):
    __tablename__="macros"

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    calories = Column(Integer)
    protein = Column(Integer)
    carbohydrates = Column(Integer)
    fats = Column(Integer)
    recipe = relationship("Recipe", back_populates="macros", uselist=False)