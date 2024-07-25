from src.mealplan.crud import create_mealplan
from src.mealdate.crud import create_mealdate

from src.models import Mealplan, Mealdate
from datetime import datetime

class TestMealplan:

    def test_create_mealplan(self, session):
        create_mealplan(session, user_id=1, title="test", createdOn=datetime(2024, 7, 24), lastUpdated=datetime(2024, 7, 24))

        mealplan = session.query(Mealplan).filter(Mealplan.id == 1).first()
        assert mealplan.author_id == 1

    def test_create_mealdates(self, session):
        create_mealdate(session, mealplan_id=1, recipe_id=1, servings=1, date=datetime(2024, 7, 25))

        mealdate = session.query(Mealdate).filter(Mealdate.mealplan_id == 1).first()
        assert mealdate.recipe_id == 1

    def test_create_multiple_mealdates(self, session):
        create_mealdate(session, mealplan_id=1, recipe_id=2, servings=1, date=datetime(2024, 7 ,26))

        mealdate = session.query(Mealdate).filter(Mealdate.recipe_id == 2).first()
        assert mealdate.mealplan_id == 1

    def test_get_all_mealdates(self, session):
        mealplan = session.query(Mealplan).get(1)

        print(mealplan.title)

        for day in mealplan.mealdates:
            print(f"{day.date}, {day.recipe_id}, {day.servings}")