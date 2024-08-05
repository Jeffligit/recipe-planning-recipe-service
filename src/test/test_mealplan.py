from src.mealplan.crud import create_mealplan
from src.meal.crud import create_meal
from src.main import add_mealplan

from src.models import Mealplan, Meal
from datetime import date

class TestMealplan:

    def test_create_mealplan(self, session):
        create_mealplan(session, user_id=1, title="test", createdOn=date(2024, 7, 24), lastUpdated=date(2024, 7, 24))

        mealplan = session.query(Mealplan).filter(Mealplan.id == 1).first()
        assert mealplan.author_id == 1

    def test_create_meals(self, session):
        create_meal(session, mealplan_id=1, recipe_id=1, servings=1, date=date(2024, 7, 25))

        meal = session.query(Meal).filter(Meal.mealplan_id == 1).first()
        assert meal.recipe_id == 1

    def test_create_multiple_meals(self, session):
        create_meal(session, mealplan_id=1, recipe_id=2, servings=1, date=date(2024, 7 ,26))

        meal = session.query(Meal).filter(Meal.recipe_id == 2).first()
        assert meal.mealplan_id == 1

    def test_get_all_meals(self, session):
        mealplan = session.query(Mealplan).get(1)

        print(mealplan.title)

        for day in mealplan.meals:
            print(f"{day.date}, {day.recipe_id}, {day.servings}")