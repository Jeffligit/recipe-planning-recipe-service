from .database import Base

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table
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
    ingredients = relationship("Quantity", back_populates="recipe")
    macros = relationship("Macro", back_populates="recipe")
    tags = relationship("Tag", secondary=recipes_tags, back_populates="recipes")


class Ingredient(Base):
    __tablename__= "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    recipes = relationship("Quantity", back_populates="ingredient")


'''
Quantity Table:

id: int
recipe_id: int
ingredient_id: int
amount: float
unit: str

Quantity table is essentially our ManyToMany association between Recipes and Ingredients
Many Ingredients in a Recipe
Many Recipes for an Ingredient

Since we need more columns than just recipes and ingredients, we need to use Association Object

Parent --> Recipe
Child --> Ingredient
'''

class Quantity(Base):
    __tablename__="quantities"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    amount = Column(Float)
    unit = Column(String, index=True)

    ingredient = relationship("Ingredient", back_populates="recipes")
    recipe = relationship("Recipe", back_populates="ingredients")


class Macro(Base):
    __tablename__="macros"

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    calories = Column(Integer)
    protein = Column(Integer)
    carbohydrates = Column(Integer)
    fats = Column(Integer)
    recipe = relationship("Recipe", back_populates="macros", uselist=False)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    tag = Column(String, index=True)
    recipes = relationship("Recipe", secondary=recipes_tags, back_populates="tags")


recipes_tags = Table(
    "recipes_tags", 
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
    )