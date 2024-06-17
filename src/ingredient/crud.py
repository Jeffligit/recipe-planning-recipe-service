from ..models import Ingredient

from sqlalchemy.orm import Session

def create_ingredient(db: Session, ingredient_id: int, ingredient_name: str):
    db_ingredient = Ingredient(id = ingredient_id, name = ingredient_name)
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient