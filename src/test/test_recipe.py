from src.recipe.crud import create_recipe, get_recipe, get_paginated_recipes
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

    def test_get_paginated_recipes(self, session):
        for i in range(10):
            test_recipe = RecipeCreate(
                title="test recipe number " + str(i + 2),
                description="some steps",
                prep_time=1,
                cook_time=1
            )
            create_recipe(session, test_recipe, user_id=i)

        #getting first 5 recipes
        recipe_list = get_paginated_recipes(session, 1, 5)

        for recipe in recipe_list:
            print(f"{recipe.id}, {recipe.title}")
        
        #getting first 2 recipes with given filter
        
        recipe_list_2 = get_paginated_recipes(session, 1, 2, Recipe.title.like("%number%"))
        for recipe in recipe_list_2:
            print(f"{recipe.id}, {recipe.title}")
        
        

'''    def test_generic_paginate_results(self, session):
        recipes = paginate_query_results(session, Recipe, Recipe.id % 2 == 0, 1, 2)

        for recipe in recipes:
            print(f"{recipe.id}, {recipe.title}")'''