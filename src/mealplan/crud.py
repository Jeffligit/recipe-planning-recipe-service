from ..models import Mealplan

from datetime import datetime

from sqlalchemy.orm import Session

def create_mealplan(db: Session, user_id: int, title: str, createdOn: datetime, lastUpdated: datetime):
    db_mealplan = Mealplan(author_id = user_id, title=title, createdOn=createdOn, lastUpdated=lastUpdated)
    db.add(db_mealplan)
    db.commit()
    db.refresh(db_mealplan)
    return db_mealplan