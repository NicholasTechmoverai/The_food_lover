from models import Recipe, RecipeStep
from reusables.main import sanitizeContents  
from uuid import  UUID

from pydantic import BaseModel, Field
from typing import List, Optional, Union


class CookTime(BaseModel):
    hr: int
    min: int


class Cuisine(BaseModel):
    name: str
    region: str


class ComplexityLevel(BaseModel):
    name: str
    value: int


class RecipeCover(BaseModel):
    id: str
    recipeName: str
    repiceColor: str
    image: str
    tags: List[str]
    cookTime: CookTime
    description: str
    cuisine: Cuisine
    complexityLevel: ComplexityLevel
    category: List[str]


class StepTimeRequired(BaseModel):
    hr: int
    min: int

class Ingredient(BaseModel):
    name: str
    amount: str
    unit: str


class Step(BaseModel):
    no: int
    timeRequired: StepTimeRequired
    tempRequired: int
    ingredientsUsed: List[Ingredient]
    instructions: str
    image: str
    videoUrl: str


class RecipeSteps(BaseModel):
    id: str
    name: str
    description: str
    category: Optional[Union[str, None]]
    ingredients: List[Ingredient]
    steps: List[Step]
    tags: List[str]


class RecipeRequest(BaseModel):
    isPublic: bool
    allowComments: bool
    copyProtection: str
    recipeCover: RecipeCover
    recipeSteps: RecipeSteps

class RecipeService:
    def __init__(self, recipe_repo=Recipe, step_repo=RecipeStep):
        self.recipe_repo = recipe_repo
        self.step_repo = step_repo

    async def create_recipe(self, data: RecipeRequest, user_id: UUID):
        """
        Creates a recipe and associated steps from the sanitized input.
        """
        # Sanitize recipe descriptions
        print("CREATING SHIT!!")
        data.recipeCover.description = sanitizeContents(data.recipeCover.description)
        data.recipeSteps.description = sanitizeContents(data.recipeSteps.description)

        for step in data.recipeSteps.steps:
            step.instructions = sanitizeContents(step.instructions)

        # Create main recipe record
        recipe = await self.recipe_repo.create(
            id=data.recipeCover.id,
            name=data.recipeCover.recipeName,
            color=data.recipeCover.repiceColor,
            image=data.recipeCover.image,
            tags=data.recipeCover.tags,
            description=data.recipeCover.description,
            cuisine=data.recipeCover.cuisine.name,
            region=data.recipeCover.cuisine.region,
            complexity=data.recipeCover.complexityLevel.name,
            complexity_value=data.recipeCover.complexityLevel.value,
            category=data.recipeCover.category,
            cook_hr=data.recipeCover.cookTime.hr,
            cook_min=data.recipeCover.cookTime.min,
            user_id=user_id,
            is_public=data.isPublic,
            allow_comments=data.allowComments,
            copy_protection=data.copyProtection
        )

        # Create steps (loop through)
        for step in data.recipeSteps.steps:
            await self.step_repo.create(
                recipe=recipe,
                no=step.no,
                temp=step.tempRequired,
                time_hr=step.timeRequired.hr,
                time_min=step.timeRequired.min,
                ingredients=step.ingredientsUsed,
                instructions=step.instructions,
                image=step.image,
                video=step.videoUrl
            )

        return recipe

    async def get_recipe_by_id(self, recipe_id: str):
        return await self.recipe_repo.get_or_none(id=recipe_id)

    async def list_recipes(self, public_only=True):
        if public_only:
            return await self.recipe_repo.filter(is_public=True)
        return await self.recipe_repo.all()
