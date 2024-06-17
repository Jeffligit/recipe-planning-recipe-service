from ..models import MealPlan
from ..schemas import MealPlanCreate

from sqlalchemy.orm import Session

def create_mealplan(db: Session, mealplan: MealPlanCreate, user_id: int):
    db_mealplan = MealPlan(**dict(mealplan), author_id=user_id)
    db.add(db_mealplan)
    db.commit()
    db.refresh(db_mealplan)
    return db_mealplan

def get_mealplan(db: Session, mealplan_id: int):
    return db.query(MealPlan).filter(MealPlan.id == mealplan_id).first()