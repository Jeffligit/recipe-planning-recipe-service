from ..models import Instruction

from sqlalchemy.orm import Session

def create_instruction(db: Session, number: int, description: str):
    db_instruction = Instruction(step_number = number, step_description = description)
    db.add(db_instruction)
    db.commit()
    db.refresh(db_instruction)
    return db_instruction