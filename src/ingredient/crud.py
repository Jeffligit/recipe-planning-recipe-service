from ..models import Ingredient

from sqlalchemy.orm import Session

def create_ingredient(db: Session, ingredient_name: str):
    db_ingredient = Ingredient(name = ingredient_name)
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient