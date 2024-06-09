from ..models import Recipe
from ..schemas import RecipeCreate

from sqlalchemy.orm import Session

def create_recipe(db: Session, recipe: RecipeCreate, user_id: int):
    db_recipe = Recipe(**dict(recipe), author_id=user_id, rating=0.0)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe
