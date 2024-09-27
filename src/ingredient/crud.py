from ..models import Ingredient

from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

def create_ingredient(db: Session, ingredient_name: str):
    db_ingredient = Ingredient(name = ingredient_name)
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def get_ingredient_by_name(db: Session, ingredient_name: str):
    return db.query(Ingredient).filter(Ingredient.name == ingredient_name).first()

def ingredient_exists_by_name(db: Session, ingredient_name: str):
    return db.query(exists().where(Ingredient.name == ingredient_name)).scalar()