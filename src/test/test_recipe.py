from src.recipe.crud import create_recipe, get_recipe
from src.main import add_full_recipe
from src.models import Recipe
from src.schemas import RecipeCreate

class TestRecipe:

    def test_create_recipe(self, session):
        test_recipe = RecipeCreate(
            title="test recipe",
            description="some steps",
            prep_time=1,
            cook_time=1
        )
        create_recipe(session, test_recipe, user_id=1)
        expected = session.query(Recipe).filter(Recipe.id == 1).first()
        assert expected.title == "test recipe"

    def test_get_recipe(self, session):
        expected = get_recipe(session, 1)
        assert expected.title == "test recipe"

    def test_create_full_recipe(self, session):
        test_recipe = RecipeCreate(
            title="Chicken Pasta",
            description="some steps",
            prep_time=1,
            cook_time=1
        )
        ingredients_list = [{'name': "Pasta", 'amount': 100, 'unit': "g"},
                            {'name': "Chicken", 'amount': 10, 'unit': "oz"},
                            {'name': "Cheese", 'amount': 50, 'unit': "g"}]
        
        instructions_list = [{'number': 1, 'description': "do this first"},
                             {'number': 2, 'description': "do this second"},
                             {'number': 3, 'description': "do this third"}]
        
        tags_list = ["Italian", "High Protein", "Simple"]

        add_full_recipe(test_recipe, session, ingredients_list, instructions_list, tags_list)

        recipe = session.query(Recipe).filter(Recipe.title == "Chicken Pasta").first()
        assert recipe.title == "Chicken Pasta"

    def test_get_full_recipe(self, session):
        recipe = session.query(Recipe).filter(Recipe.title == "Chicken Pasta").first()

        for quantity in recipe.quantities:
            print(f"{quantity.ingredient_id}, {quantity.ingredient.name}, {quantity.amount}, {quantity.unit}")

        for step in recipe.instructions:
            print(f"Step: {step.step_number}, {step.step_description}")

        for tag in recipe.tags:
            print(f"Tag: {tag.name}")
        
    def test_create_multiple_full_recipes(self, session):
        test_recipe = RecipeCreate(
            title="Chicken Fried Rice",
            description="some steps",
            prep_time=1,
            cook_time=1
        )

        ingredients_list = [{'name': "Rice", 'amount': 200, 'unit': "g"},
                            {'name': "Chicken", 'amount': 100, 'unit': "g"},
                            {'name': "Egg", 'amount': 3, 'unit': "count"}]
        
        instructions_list = [{'number': 1, 'description': "do this first"},
                             {'number': 2, 'description': "do this second"},
                             {'number': 3, 'description': "do this third"}]
        
        tags_list = ["Asian", "Simple"]

        add_full_recipe(test_recipe, session, ingredients_list, instructions_list, tags_list)

        recipe = session.query(Recipe).filter(Recipe.title == "Chicken Fried Rice").first()
        assert recipe.title == "Chicken Fried Rice"
        for quantity in recipe.quantities:
            print(f"{quantity.ingredient_id}, {quantity.ingredient.name}, {quantity.amount}, {quantity.unit}")

        for step in recipe.instructions:
            print(f"Step: {step.step_number}, {step.step_description}")

        for tag in recipe.tags:
            print(f"Tag: {tag.name}")