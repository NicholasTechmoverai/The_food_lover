from models import Recipe, RecipeStep, Tag, Category,Ingredient
from reusables.main import sanitizeContents ,save_base64_image
from uuid import  UUID
from tortoise.expressions import Q

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
    value: str


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

class IngredientInStep(BaseModel):
    name: str
    amount: str
    unit: str


class Step(BaseModel):
    no: int
    timeRequired: StepTimeRequired
    tempRequired: int
    ingredientsUsed: List[IngredientInStep]
    instructions: str
    image: str
    videoUrl: str


class RecipeSteps(BaseModel):
    id: str
    name: str
    description: str
    category: Optional[Union[str, None]]
    ingredients: List[IngredientInStep]
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

    async def create_or_update_recipe(self, data: RecipeRequest, user_id: UUID):
        # 1. Sanitize input
        data.recipeCover.description = sanitizeContents(data.recipeCover.description)
        data.recipeSteps.description = sanitizeContents(data.recipeSteps.description)
        for step in data.recipeSteps.steps:
            step.instructions = sanitizeContents(step.instructions)

        # 2. Check if recipe exists
        recipe = await self.recipe_repo.get_or_none(id=data.recipeCover.id)

        if recipe:
            # Fetch steps and ingredients to prevent "NoValuesFetched" errors
            await recipe.fetch_related("steps__ingredients")

            # 3. Update existing recipe
            recipe.name = data.recipeCover.recipeName
            recipe.description = data.recipeCover.description
            recipe.theme_color = data.recipeCover.repiceColor
            recipe.cover_image_url = await save_base64_image(data.recipeCover.image, 'uploads')
            recipe.cuisine = data.recipeCover.cuisine.name
            recipe.difficulty_level = data.recipeCover.complexityLevel.value
            recipe.cook_time_minutes = data.recipeCover.cookTime.hr * 60 + data.recipeCover.cookTime.min
            recipe.user_id = user_id
            recipe.is_public = data.isPublic
            recipe.allow_comments = data.allowComments
            recipe.copy_protection = data.copyProtection
            await recipe.save()

            # Clear tags/categories
            await recipe.tags.clear()
            await recipe.category.clear()

            # Delete old steps & their ingredients
            for step in recipe.steps:
                await step.ingredients.all().delete()
                await step.delete()

        else:
            # 4. Create new recipe
            recipe = await self.recipe_repo.create(
                id=data.recipeCover.id,
                name=data.recipeCover.recipeName,
                description=data.recipeCover.description,
                theme_color=data.recipeCover.repiceColor,
                cover_image_url=await save_base64_image(data.recipeCover.image, 'uploads'),
                cuisine=data.recipeCover.cuisine.name,
                difficulty_level=data.recipeCover.complexityLevel.value,
                cook_time_minutes=data.recipeCover.cookTime.hr * 60 + data.recipeCover.cookTime.min,
                user_id=user_id,
                is_public=data.isPublic,
                allow_comments=data.allowComments,
                copy_protection=data.copyProtection
            )

        # 5. Add tags
        for tag_name in data.recipeCover.tags:
            tag = await Tag.get_or_none(name=tag_name) or await Tag.create(name=tag_name)
            await recipe.tags.add(tag)

        # 6. Add categories
        for category_name in data.recipeCover.category:
            category = await Category.get_or_none(name=category_name) or await Category.create(name=category_name)
            await recipe.category.add(category)

        # 7. Create steps and ingredients
        for step_data in data.recipeSteps.steps:
            step = await RecipeStep.create(
                recipe=recipe,
                step_number=step_data.no,
                cook_time_minutes=step_data.timeRequired.hr * 60 + step_data.timeRequired.min,
                temperature_celsius=step_data.tempRequired,
                description=step_data.instructions,
                image_url=await save_base64_image(step_data.image, 'uploads'),
                video_url=step_data.videoUrl
            )

            for ing in step_data.ingredientsUsed:
                await Ingredient.create(
                    name=ing.name,
                    quantity=ing.amount,
                    unit=ing.unit,
                    recipe_step=step
                )

        return recipe

    async def get_recipe_by_id(self, recipe_id: UUID):
        return await self.recipe_repo.get_or_none(id=recipe_id).prefetch_related("tags", "category", "steps__ingredients")


    async def list_recipes(self, public_only=True, limit: int = 10, offset: int = 0):
        query = self.recipe_repo.all().prefetch_related("tags", "category", "steps__ingredients", "user")

        if public_only:
            query = query.filter(is_public=True)

        query = query.order_by("-updated_at", "-created_at").offset(offset).limit(limit)
        recipes = await query

        def minutes_to_time(cook_time_minutes):
            return {
                "hr": cook_time_minutes // 60,
                "min": cook_time_minutes % 60
            }

        result = []
        for r in recipes:
            recipe_dict = {
                "id": str(r.id),
                "recipeName": r.name,
                "repiceColor": r.theme_color,
                "image": r.cover_image_url,
                "tags": [tag.name for tag in r.tags],
                "cookTime": minutes_to_time(r.cook_time_minutes),
                "description": r.description,
                "cuisine": {
                    "name": r.cuisine,
                    "region": "East Africa"  # You can modify this to come from DB if available
                },
                "complexityLevel": {
                    "name": r.difficulty_level.capitalize(),
                    "value": {"Easy": 1, "Medium": 2, "Hard": 3}.get(r.difficulty_level.capitalize(), 1)
                },
                "category": [cat.name for cat in r.category],
                "user": {
                    "name": r.user.name if hasattr(r.user, "name") else "Unknown",
                    "profilePic": getattr(r.user, "profile_pic", ""),
                    "id": str(r.user.id),
                    "totalRecipes": await self.recipe_repo.filter(user=r.user).count(),
                    "isVerified": getattr(r.user, "is_verified", False),
                }
            }
            result.append(recipe_dict)

        return result
