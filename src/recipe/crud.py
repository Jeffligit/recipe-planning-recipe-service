from ..models import Recipe
from ..schemas import RecipeCreate

from sqlalchemy.orm import Session

def create_recipe(db: Session, recipe: RecipeCreate, user_id: int):
    db_recipe = Recipe(**dict(recipe), author_id=user_id, rating=0.0)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_recipe(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()

def get_paginated_recipes(db: Session, page: int, per_page: int):
    return db.query(Recipe).limit(per_page).offset((page - 1) * per_page).all()