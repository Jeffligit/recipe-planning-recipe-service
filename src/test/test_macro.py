from src.macro.crud import create_macro, get_macro_from_recipe
from src.recipe.crud import create_recipe
from src.models import Macro, Recipe
from src.schemas import MacroCreate, RecipeCreate

class TestMacro:

    def test_create_macro(self, session):

        test_recipe = RecipeCreate(
            title="test recipe",
            description="some steps",
            prep_time=1,
            cook_time=1
        )
        create_recipe(session, test_recipe, user_id=1)
        test_macro = MacroCreate(
            calories=170,
            protein=10,
            carbohydrates=10,
            fats=10
        )
        create_macro(session, test_macro, recipe_id=1)
        expected = session.query(Macro).filter(Macro.id == 1).first()
        assert expected.calories == 170

    def testing_get_macro_from_recipe_relationship(self, session):

        expectedRecipe = session.query(Recipe).filter(Recipe.id == 1).first()
        #print(f"Recipe: {expectedRecipe.macros.calories}")
        assert expectedRecipe.macros.calories == 170



    def testing_get_recipe_from_macro_relationship(self, session):
        expectedMacro = session.query(Macro).filter(Macro.id == 1).first()
        #print(expectedMacro.recipe.title)
        assert expectedMacro.recipe.title == "test recipe"