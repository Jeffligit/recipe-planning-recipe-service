from sqlalchemy.orm import Session
from sqlalchemy import asc, desc


def get_paginated_results(db: Session, page: int, per_page: int, model, filter=None, isAscending=None, sortBy=None):
    '''
    Parameters:
        page, per_page: for paginating
        model: Table name to query
        sortBy: Optional criteria to order the results by
        isAscending: If true, order by ascending, if false, order by descending
        filter: Optional filter for all results
    '''
    
    query = db.query(model)
    if filter is not None:
        query = query.filter(filter)

    if sortBy is not None:
        if isAscending:
            query = query.order_by(asc(sortBy))
        else:
            query = query.order_by(desc(sortBy))
    
    return query.limit(per_page).offset((page - 1) * per_page).all()

def edit_field(db: Session, model, id, field_to_edit, new_value):
    entry = db.query(model).get(id)

    if entry is None:
        raise ValueError(f"No instance found with id {id}")
    
    setattr(entry, field_to_edit, new_value)

    db.commit()

    return entry
    