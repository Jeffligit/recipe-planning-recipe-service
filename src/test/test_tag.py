from src.tag.crud import create_tag
from src.recipe.crud import create_recipe
from src.models import Tag, Recipe
from src.schemas import RecipeCreate

class TestTag:

    def test_create_tag(self, session):
        test_recipe = RecipeCreate(
            title="Pasta",
            description="some steps",
            prep_time=1,
            cook_time=1
        )
        create_recipe(session, test_recipe, user_id=1)
        tag = create_tag(session, "Italian")

        recipe = session.query(Recipe).filter(Recipe.id == 1).first()
        
        recipe.tags.append(tag)

        assert recipe.title == "Pasta"
    
    def test_get_tag_from_recipe(self, session):
        recipe = session.query(Recipe).filter(Recipe.title == "Pasta").first()
        print(recipe.title)
        for tag in recipe.tags:
            print(f"Tag: {tag.name}")
            assert tag.name == "Italian"

    def test_multiple_tags_for_recipe(self, session):
        tag2 = create_tag(session, "Low Calorie")
        tag3 = create_tag(session, "High Protein")

        recipe = session.query(Recipe).filter(Recipe.title == "Pasta").first()

        recipe.tags.append(tag2)
        recipe.tags.append(tag3)

        for tag in recipe.tags:
            print(f"Tag: {tag.id}, {tag.name}")
        
        assert len(recipe.tags) == 3

    def test_multiple_recipes_for_tag(self, session):
        test_recipe = RecipeCreate(
            title="Pizza",
            description="some steps",
            prep_time=1,
            cook_time=1
        )
        recipe = create_recipe(session, test_recipe, 1)

        tag = session.query(Tag).filter(Tag.name == "Italian").first()

        recipe.tags.append(tag)

        for recipe in tag.recipes:
            print(f"Recipe: {recipe.id}, {recipe.title}")

        assert len(tag.recipes) == 2
