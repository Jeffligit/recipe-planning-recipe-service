from src.quantity.crud import create_quantity
from src.recipe.crud import create_recipe
from src.ingredient.crud import create_ingredient
from src.models import Quantity, Recipe, Ingredient
from src.schemas import RecipeCreate

class TestQuantity:
    
    def test_create_quantity(self, session):
        test_recipe = RecipeCreate(
            title="chicken parm",
            description="some steps",
            prep_time=1,
            cook_time=1
        )

        create_recipe(session, test_recipe, user_id=1)
        create_ingredient(session, ingredient_name="chicken")

        expectedIngredient = session.query(Ingredient).filter(Ingredient.id == 1).first()
        #assert expectedIngredient.name == "chicken"
        
        create_quantity(session, 1, expectedIngredient.id, 10, "oz")

        expected = session.query(Quantity).filter(Quantity.recipe_id == 1).first()
        assert expected.ingredient_id == 1

    def test_add_multiple_ingredients(self, session):

        # Multiple ingredients for Recipe 1
                
        create_ingredient(session, ingredient_name="pasta")
        expectedIngredient = session.query(Ingredient).filter(Ingredient.name == "pasta").first()

        create_quantity(session, 1, expectedIngredient.id, 100, "g")

        expected = session.query(Quantity).filter(Quantity.ingredient_id == expectedIngredient.id).first()
        assert expected.amount == 100

    def test_get_all_quantities_for_recipe(self, session):

        # Geting all ingredients + quantities for Recipe 1
    
        recipe = session.query(Recipe).filter(Recipe.id == 1).first()
        print(recipe.title)

        for quantity in recipe.quantities:
            print(f"{quantity.ingredient_id}, {quantity.ingredient.name}, {quantity.amount}, {quantity.unit}")
        
        assert recipe.id == 1

    def test_get_all_quantities_for_ingredient(self, session):

        # Multiple recipes for Ingredient 1

        test_recipe = RecipeCreate(
            title="chicken sandwich",
            description="some steps",
            prep_time=1,
            cook_time=1
        )
        create_recipe(session, test_recipe, 1)
        create_quantity(session, 2, 1, 8, "oz")

        ingredient = session.query(Ingredient).filter(Ingredient.name == "chicken").first()

        # Getting all recipes + quantities for Ingredient 1
        
        for quantity in ingredient.quantities:
            print(f"{quantity.recipe_id}, {quantity.recipe.title}, {quantity.amount}")

        assert len(ingredient.quantities) == 2