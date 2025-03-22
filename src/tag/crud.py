from ..models import Tag

from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

def create_tag(db: Session, tag: str):
    db_tag = Tag(name = tag)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def tag_exists_by_name(db: Session, tag: str):
    return db.query(exists().where(Tag.name == tag)).scalar()

def get_tag(db: Session, tag: str):
    return db.query(Tag).filter(Tag.name == tag).first()