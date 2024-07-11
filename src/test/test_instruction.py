from src.instruction.crud import create_instruction
from src.recipe.crud import create_recipe
from src.models import Recipe
from src.schemas import RecipeCreate

class TestInstruction:

    def test_create_instruction(self, session):
        test_recipe = RecipeCreate(
            title="test recipe",
            description="details",
            prep_time=1,
            cook_time=1
        )
        recipe = create_recipe(session, test_recipe, user_id=1)
        step = create_instruction(session, 1, "do this first")

        recipe.instructions.append(step)

        assert step.step_description == "do this first"
    
    
    def test_get_instructions(self, session):
        recipe = session.query(Recipe).filter(Recipe.id == 1).first()

        for step in recipe.instructions:
            print(f"Step: {step.step_number}, {step.step_description}")

    def test_add_multiple_instructions(self, session):
        recipe = session.query(Recipe).filter(Recipe.id == 1).first()

        step2 = create_instruction(session, 2, "do this second")
        step3 = create_instruction(session, 3, "do this last")

        recipe.instructions.append(step2)
        recipe.instructions.append(step3)

    def test_get_multiple_instructions(self, session):
        recipe = session.query(Recipe).filter(Recipe.id == 1).first()

        for step in recipe.instructions:
            print(f"Step: {step.step_number}, {step.step_description}")

        assert len(recipe.instructions) == 3