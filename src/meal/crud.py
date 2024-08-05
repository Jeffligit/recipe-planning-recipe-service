from ..models import Meal
from datetime import datetime

from sqlalchemy.orm import Session

def create_meal(db: Session, mealplan_id: int, recipe_id: int, servings: int, date: datetime):
    db_meal = Meal(mealplan_id=mealplan_id, recipe_id=recipe_id, servings=servings, date=date)
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal