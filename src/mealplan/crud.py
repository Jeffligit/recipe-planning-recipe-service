from ..models import Mealplan

from datetime import date

from sqlalchemy.orm import Session

def create_mealplan(db: Session, user_id: int, title: str, createdOn: date, lastUpdated: date):
    db_mealplan = Mealplan(author_id = user_id, title=title, createdOn=createdOn, lastUpdated=lastUpdated)
    db.add(db_mealplan)
    db.commit()
    db.refresh(db_mealplan)
    return db_mealplan

def get_mealplan(db: Session, mealplan_id: int):
    return db.query(Mealplan).get(mealplan_id)