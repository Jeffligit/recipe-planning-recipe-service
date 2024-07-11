from ..models import Quantity

from sqlalchemy.orm import Session

def create_quantity(db: Session, recipe_id: int, ingredient_id: int, amount: float, unit: str):
    db_quantity = Quantity(recipe_id=recipe_id, ingredient_id=ingredient_id, amount=amount, unit=unit)
    db.add(db_quantity)
    db.commit()
    db.refresh(db_quantity)
    return db_quantity