from ..models import Macro
from ..schemas import MacroCreate

from sqlalchemy.orm import Session

def create_macro(db: Session, macro: MacroCreate, recipe_id: int):
    db_macro = Macro(**dict(macro), recipe_id=recipe_id)
    db.add(db_macro)
    db.commit()
    db.refresh(db_macro)
    return db_macro

def get_macro_from_recipe(db: Session, recipe_id: int):
    return db.query(Macro).filter(Macro.recipe_id == recipe_id).all()