from ..models import Mealdate
from datetime import datetime

from sqlalchemy.orm import Session

def create_mealdate(db: Session, mealplan_id: int, recipe_id: int, servings: int, date: datetime):
    db_mealdate = Mealdate(mealplan_id=mealplan_id, recipe_id=recipe_id, servings=servings, date=date)
    db.add(db_mealdate)
    db.commit()
    db.refresh(db_mealdate)
    return db_mealdate