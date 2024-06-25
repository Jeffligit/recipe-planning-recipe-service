
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base


@pytest.fixture(scope="class")
def session():
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    test_db = Session()
    Base.metadata.create_all(engine)
    try:
        yield test_db
    finally:
        Base.metadata.drop_all(engine)
        test_db.close()

