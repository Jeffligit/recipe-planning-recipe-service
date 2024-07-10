from ..models import Tag

from sqlalchemy.orm import Session

def create_tag(db: Session, tag: str):
    db_tag = Tag(name = tag)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag