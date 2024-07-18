from src.recipe.crud import create_recipe
from src.util_crud import get_paginated_results, edit_field
from src.ingredient.crud import create_ingredient
from src.models import Recipe, Ingredient
from src.schemas import RecipeCreate

class TestUtil:

    def test_create_recipes(self, session):
        for i in range(1, 11):
            test_recipe = RecipeCreate(
                title="test recipe number " + str(i),
                description="some steps",
                prep_time=1,
                cook_time=1
            )
            create_recipe(session, test_recipe, 1)

    def test_get_paginated_recipes(self, session):
        #getting first 3 recipes, no filter, no sort
        recipe_list = get_paginated_results(session, 1, 3, Recipe)

        for recipe in recipe_list:
            print(f"{recipe.id}, {recipe.title}")

        assert len(recipe_list) == 3

    def test_get_filtered_paginated_recipes(self, session):
        #getting first 3 recipes, even ids filter
        recipe_list = get_paginated_results(session, 1, 3, Recipe, Recipe.id % 2 == 0)

        for recipe in recipe_list:
            print(f"{recipe.id}, {recipe.title}")
            assert recipe.id % 2 == 0
        
        assert len(recipe_list) == 3

    def test_get_ordered_filtered_paginated_recipes(self, session):
        #getting first 3 recipes, even ids filter, order by id descending
        recipe_list = get_paginated_results(session, 1, 3, Recipe, Recipe.id % 2 == 0, False, Recipe.id)

        for recipe in recipe_list:
            print(f"{recipe.id}, {recipe.title}")
            assert recipe.id % 2 == 0

        assert len(recipe_list) == 3


    def test_create_ingredients(self, session):
        for i in range(1, 11):
            create_ingredient(session, i, str(11-i) + "name")

    def test_get_paginated_ingredients(self, session):
        ingredient_list = get_paginated_results(session, 1, 3, Ingredient)

        for ing in ingredient_list:
            print(f"{ing.id}, {ing.name}")

    def test_get_filtered_paginated_ingredients(self, session):
        ingredient_list = get_paginated_results(session, 1, 3, Ingredient, Ingredient.id % 2 == 1)

        for ing in ingredient_list:
            print(f"{ing.id}, {ing.name}")

    def test_get_ordered_filtered_paginated_ingredients(self, session):
        ingredient_list = get_paginated_results(session, 1, 3, Ingredient, Ingredient.id % 2 == 1, True, Ingredient.name)

        for ing in ingredient_list:
            print(f"{ing.id}, {ing.name}")
    
    def test_edit(self, session):
        new_recipe = edit_field(session, Recipe, 1, "title", "new title")
        new_ingredient = edit_field(session, Ingredient, 5, "name", "new ingredient")
        print(new_recipe.title)
        print(new_ingredient.name)