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
    mealplans = relationship("MealPlan", back_populates="author")


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

class MealPlan(Base):
    __tablename__ = "mealplans"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    ingredients = Column(String, index=True)
    author = relationship("User", back_populates="mealplans")
