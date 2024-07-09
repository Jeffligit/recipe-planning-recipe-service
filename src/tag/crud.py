from ..models import Tag

from sqlalchemy.orm import Session

def create_tag(db: Session, tag_id: int, tag: str):
    db_tag = Tag(id = tag_id, tag = tag)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag