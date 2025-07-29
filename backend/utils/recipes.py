from models import (
    Recipe,
    RecipeStep,
    Tag,
    Category,
    Ingredient,
    RecipeLike,
    RecipeComment,
    ShareRecipe,
    Favorite,
    RecipeView,
    Follow,
    Notification,
    CommentLike,
)
from reusables.main import sanitizeContents, save_base64_image, sanitize_name,clean_and_truncate
from uuid import UUID
from typing import Tuple
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException
from typing import Any
import os
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from tortoise.expressions import Q
from tortoise.functions import Count
from itertools import islice
from datetime import datetime, timedelta, timezone
import random
from config import Config, BASE_SERVER,WEB_SERVER
from tortoise.expressions import Q
from collections import defaultdict

from .logger import setup_logger

logger = setup_logger("RECIPES")


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
    name: Optional[str] = None
    amount: Optional[str] = None
    unit: Optional[str] = None


class Step(BaseModel):
    no: int
    timeRequired: Optional[StepTimeRequired] = None
    tempRequired: Optional[int] = None
    ingredientsUsed: Optional[List[IngredientInStep]] = []
    instructions: Optional[str] = None
    image: str
    videoUrl: Optional[str] = None


class RecipeSteps(BaseModel):
    id: str
    name: str
    description: str
    category: Optional[list[str]] = None
    ingredients: Optional[List[IngredientInStep]] = []
    steps: Optional[List[Step]] = []
    tags: Optional[List[str]] = []


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

    async def create_or_update_recipe(
        self, data: RecipeRequest, user_id: UUID, user_name
    ):
        upload_path = os.path.join(Config.CHEF_PATH, await sanitize_name(user_name))

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
            recipe.cover_image_url = await save_base64_image(
                data.recipeCover.image, upload_path
            )
            recipe.cuisine = data.recipeCover.cuisine.name
            recipe.difficulty_level = data.recipeCover.complexityLevel.value
            recipe.cook_time_minutes = (
                data.recipeCover.cookTime.hr * 60 + data.recipeCover.cookTime.min
            )
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
                cover_image_url=await save_base64_image(
                    data.recipeCover.image, upload_path
                ),
                cuisine=data.recipeCover.cuisine.name,
                difficulty_level=data.recipeCover.complexityLevel.value,
                cook_time_minutes=data.recipeCover.cookTime.hr * 60
                + data.recipeCover.cookTime.min,
                user_id=user_id,
                is_public=data.isPublic,
                allow_comments=data.allowComments,
                copy_protection=data.copyProtection,
            )

        # 5. Add tags
        for tag_name in data.recipeCover.tags:
            tag = await Tag.get_or_none(name=tag_name) or await Tag.create(
                name=tag_name
            )
            await recipe.tags.add(tag)

        # 6. Add categories
        for category_name in data.recipeCover.category:
            category = await Category.get_or_none(
                name=category_name
            ) or await Category.create(name=category_name)
            await recipe.category.add(category)

        # 7. Create steps and ingredients
        for step_data in data.recipeSteps.steps:
            step = await RecipeStep.create(
                recipe=recipe,
                step_number=step_data.no,
                cook_time_minutes=step_data.timeRequired.hr * 60
                + step_data.timeRequired.min,
                temperature_celsius=step_data.tempRequired,
                description=step_data.instructions,
                image_url=await save_base64_image(step_data.image, upload_path),
                video_url=step_data.videoUrl,
            )

            for ing in step_data.ingredientsUsed:
                await Ingredient.create(
                    name=ing.name, quantity=ing.amount, unit=ing.unit, recipe_step=step
                )

        followers = await Follow.filter(following_id=user_id).prefetch_related(
            "follower"
        )
        follower_ids = [f.follower.id for f in followers]
        for uid in follower_ids:
            notification = await Notification.create(
                user_id=uid,
                actor_id=user_id,
                notification_type="new_recipe",
                target_object_id=str(recipe.id),
                target_content_type="recipe",
                verb=f"published a new recipe '{data.recipeCover.recipeName or recipe.name}'",
                thread_id=None,
                preview=recipe.name,
            )
            # Try to import and trigger WebSocket notification
            try:
                from app import notifications_namespace

                noty = await Notification.filter(id=notification.id).prefetch_related(
                    "user", "actor"
                )

                await notifications_namespace.trigger_notification({
                    "user_id": str(uid),
                    "notifications": noty,
                })

            except ImportError as e:
                # Optionally log this exception
                logger.info(f"WebSocket notification import failed: {e}")

        return recipe

    async def minutes_to_time(self, cook_time_minutes):
        return {"hr": cook_time_minutes // 60, "min": cook_time_minutes % 60}

    async def list_recipes(
        self,
        public_only: bool = True,
        limit: int = 10,
        offset: int = 0,
        user_id: Optional[UUID] = None,
        saved: Optional[bool] = False,
        tags: Optional[list] = None,
        name: Optional[str] = None,
        cuisine: Optional[str] = None,
        category: Optional[list] = None,
    ):
        logger.info(
            "FILTERS — public: %s | user_id: %s | saved: %s | name: %s | cuisine: %s | tags: %s | category: %s",
            public_only,
            user_id,
            saved,
            name,
            cuisine,
            tags,
            category,
        )

        query = self.recipe_repo.all().prefetch_related(
            "tags", "category", "steps__ingredients", "user"
        )

        if public_only:
            query = query.filter(is_public=True)

        if saved and user_id:
            saved_ids = await Favorite.filter(user_id=user_id).values_list(
                "recipe_id", flat=True
            )
            logger.info("Saved recipe IDs: %s", saved_ids)
            query = query.filter(id__in=saved_ids)
        elif user_id:
            query = query.filter(user_id=user_id)

        # Construct OR filters
        or_filter = Q()

        if name and name.strip():
            or_filter |= Q(name__icontains=name.strip())

        if cuisine and cuisine.strip():
            or_filter |= Q(cuisine__icontains=cuisine.strip())

        if category and isinstance(category, list):
            for cat in category:
                if cat and isinstance(cat, str):
                    or_filter |= Q(category__name__icontains=cat.strip())

        if tags and isinstance(tags, list):
            for tag in tags:
                if tag and isinstance(tag, str):
                    or_filter |= Q(tags__name__icontains=tag.strip())

        # Apply the combined OR filter
        if or_filter:
            query = query.filter(or_filter)

        query = query.order_by("-updated_at", "-created_at").offset(offset).limit(limit)
        recipes = await query
        recipes = list({recipe.id: recipe for recipe in recipes}.values())

        logger.info("Final recipe count: %s", len(recipes))

        # Format results

        result = []
        for r in recipes:
            result.append({
                "id": str(r.id),
                "recipeName": r.name,
                "createdAt": r.created_at,
                "repiceColor": r.theme_color,
                "image": f"{BASE_SERVER}/{r.cover_image_url}",
                "tags": [tag.name for tag in r.tags],
                "cookTime": await self.minutes_to_time(r.cook_time_minutes),
                "description": r.description,
                "cuisine": {"name": r.cuisine, "region": "East Africa"},
                "complexityLevel": {
                    "name": r.difficulty_level.capitalize(),
                    "value": {"Easy": 1, "Medium": 2, "Hard": 3}.get(
                        r.difficulty_level.capitalize(), 1
                    ),
                },
                "category": [cat.name for cat in r.category],
                "user": {
                    "username": getattr(r.user, "username", "Unknown"),
                    "name": getattr(r.user, "name", "Unknown"),
                    "profilePic": r.user.picture_url
                    if r.user.picture_url.startswith("https://")
                    else f"{BASE_SERVER}/{r.user.picture_url}",
                    "id": str(r.user.id),
                    "totalRecipes": await self.recipe_repo.filter(user=r.user).count(),
                    "isVerified": getattr(r.user, "is_verified", False),
                },
            })

        return {"recipes": result, "limit": limit, "offset": offset}

    async def get_recipes_suggestions(self, name: str,return_unsimilar:bool=True,return_no:int=10):
        query = self.recipe_repo.all().prefetch_related(
            "tags", "category", "steps__ingredients", "user", "views", "likes"
        )

        or_filter = Q()

        if name and name.strip():
            name = name.strip()
            or_filter |= Q(name__icontains=name)
            or_filter |= Q(cuisine__icontains=name)
            or_filter |= Q(category__name__icontains=name)
            or_filter |= Q(tags__name__icontains=name)

            filtered_recipes = await query.filter(or_filter).distinct().limit(10)
        else:
            filtered_recipes = []

        count_found = len(filtered_recipes)

        # If we found less than 10, fetch top-rated to fill the gap
        if count_found < return_no and return_unsimilar:
            filler_limit = return_no - count_found

            filler_recipes = (
                await self.recipe_repo.all()
                .prefetch_related(
                    "tags", "category", "steps__ingredients", "user", "views", "likes"
                )
                .annotate(total_views=Count("views"), total_likes=Count("likes"))
                .order_by("-total_views", "-total_likes")
                .exclude(id__in=[recipe.id for recipe in filtered_recipes])
                .limit(filler_limit)
            )

            filtered_recipes.extend(filler_recipes)

        return [
            {
                "title": recipe.name[:30],
                "description": clean_and_truncate(recipe.description[:50]),
                "image": f"{BASE_SERVER}/{recipe.cover_image_url}" or "",
                "alt": f"{recipe.name} by {recipe.user.name}",
                "views": await recipe.views.all().count(),
                "likes": await recipe.likes.all().count(),
                "theme":recipe.theme_color,
                "url": f"/recipes/{recipe.name.strip().lower().replace(' ', '-')}/{recipe.id}",
                "out_url":f"{WEB_SERVER}/recipes/{recipe.name.strip().lower().replace(' ', '-')}/{recipe.id}",
                "cook_time": await self.minutes_to_time(recipe.cook_time_minutes),
                "difficulty_level": recipe.difficulty_level,
                "cuisine": {"name": recipe.cuisine, "region": "East Africa"},
                "chef": {
                    "id": str(recipe.user.id),
                    "name": recipe.user.username,
                    "avatar": recipe.user.picture_url
                    if recipe.user.picture_url.startswith("https://")
                    else f"{BASE_SERVER}/{recipe.user.picture_url}",
                    "theme": recipe.user.theme if hasattr(recipe.user, "theme") else "",
                },
            }
            for recipe in filtered_recipes
        ]

    async def update_view_activity(
        self, user_id: UUID, recipe_id: UUID, active_time: Optional[float] = None
    ) -> bool:
        """
        Create or update a user's view activity for a specific recipe.

        - If a view already exists, update its `active_duration`.
        - Otherwise, create a new view record.

        Args:
            user_id (UUID): ID of the viewing user.
            recipe_id (UUID): ID of the recipe being viewed.
            active_time (float, optional): Time in seconds the user was active on the recipe.

        Returns:
            bool: True if the view was created or updated successfully.
        """
        view_record, _created = await RecipeView.get_or_create(
            user_id=user_id,
            recipe_id=recipe_id,
        )

        if active_time is not None:
            view_record.active_time = int(active_time)

        await view_record.save()
        return True

    async def get_recipe_by_id(
        self, name: str, recipe_id: UUID, user_id: Optional[UUID] = None
    ) -> Tuple[dict[str, Any], dict[str, Any]]:
        try:
            recipe = await self.recipe_repo.get_or_none(id=recipe_id).prefetch_related(
                "tags", "category", "steps__ingredients", "user"
            )

            if not recipe:
                logger.warning("Recipe with ID %s not found", recipe_id)
                raise HTTPException(status_code=404, detail="Recipe not found")

            def minutes_to_time(total: int) -> dict:
                return {"hr": total // 60, "min": total % 60}

            recipe_cover = {
                "id": str(recipe.id),
                "recipeName": recipe.name,
                "repiceColor": recipe.theme_color,
                "image": f"{BASE_SERVER}/{recipe.cover_image_url}"
                if recipe.cover_image_url
                else "",
                "tags": [tag.name for tag in recipe.tags],
                "cookTime": minutes_to_time(recipe.cook_time_minutes or 0),
                "updatedAt": recipe.updated_at.isoformat(),
                "createdAt": recipe.created_at.isoformat(),
                "description": recipe.description,
                "allow_comments": recipe.allow_comments,
                "cuisine": {
                    "name": recipe.cuisine,
                    "region": "East Africa",  # Replace with dynamic region if needed
                },
                "complexityLevel": {
                    "name": recipe.difficulty_level.capitalize(),
                    "value": recipe.difficulty_level,
                },
                "category": [cat.name for cat in recipe.category],
                "user": {
                    "name": getattr(recipe.user, "name", "Unknown"),
                    "username": getattr(recipe.user, "username", "unknown"),
                    "profilePic": (
                        recipe.user.picture_url
                        if recipe.user.picture_url.startswith("https://")
                        else f"{BASE_SERVER}/{recipe.user.picture_url}"
                    )
                    if recipe.user.picture_url
                    else "",
                    "id": str(recipe.user.id),
                    "totalRecipes": await self.recipe_repo.filter(
                        user=recipe.user
                    ).count(),
                    "isVerified": getattr(recipe.user, "is_verified", False),
                },
            }

            recipe_steps = {
                "id": str(recipe.id),
                "name": recipe.name,
                "description": recipe.description,
                "category": [cat.name for cat in recipe.category],
                "tags": [tag.name for tag in recipe.tags],
                "steps": [],
            }

            for step in sorted(recipe.steps, key=lambda s: s.step_number):
                ingredients_used = [
                    {"name": ing.name, "amount": ing.quantity, "unit": ing.unit}
                    for ing in step.ingredients
                ]

                step_entry = {
                    "no": step.step_number,
                    "timeRequired": minutes_to_time(step.cook_time_minutes or 0),
                    "tempRequired": step.temperature_celsius,
                    "instructions": step.description,
                    "image": f"{BASE_SERVER}/{step.image_url}"
                    if step.image_url
                    else "",
                    "videoUrl": step.video_url,
                    "ingredientsUsed": ingredients_used,
                }

                recipe_steps["steps"].append(step_entry)

            return recipe_cover, recipe_steps

        except HTTPException:
            raise  # Re-raise FastAPI HTTP exceptions
        except Exception as e:
            logger.exception("Failed to fetch recipe ID %s: %s", recipe_id, str(e))
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while retrieving the recipe.",
            )

    async def like_unlike(self, user_id: UUID, recipe_id: UUID) -> bool:
        """
        Toggles like/unlike for a given recipe by a user.

        Returns:
            True if liked, False if unliked.
        """
        try:
            # Try to get or create a like entry
            like, created = await RecipeLike.get_or_create(
                user_id=user_id, recipe_id=recipe_id
            )

            if not created:
                # Already liked → Unlike it
                await like.delete()

                await Notification.filter(
                    actor_id=user_id,
                    notification_type="like",
                    target_object_id=str(recipe_id),
                    target_content_type="recipe",
                ).delete()

                return False

            # Get the recipe and its owner
            recipe = await Recipe.get(id=recipe_id).prefetch_related("user")

            if not recipe or not recipe.user:
                logger.error(
                    f"[Like/Unlike] Recipe or recipe.user not found for ID {recipe_id}"
                )
                return True  # Like was created even if notification fails

            chef = recipe.user

            # Don't notify self
            if chef.id != user_id:
                try:
                    # Create notification
                    notification = await Notification.create(
                        user_id=chef.id,
                        actor_id=user_id,
                        notification_type="like",
                        target_object_id=str(recipe_id),
                        target_content_type="recipe",
                        verb=f"liked your recipe '{recipe.name[:100]}'",
                        preview=recipe.name[:100],
                        thread_id=recipe.id,
                    )

                    # Trigger live notification
                    from app import notifications_namespace

                    noty = await Notification.filter(
                        id=notification.id
                    ).prefetch_related("user", "actor")

                    await notifications_namespace.trigger_notification({
                        "user_id": str(chef.id),
                        "notifications": noty,
                    })

                except Exception as e:
                    logger.warning(f"[Notification Create] Failed to create/send: {e}")

            return True

        except Exception as e:
            logger.error(f"[Like/Unlike] Unexpected error: {e}")
            return False

    async def like_unlike_favourite(self, user_id: UUID, recipe_id: UUID) -> bool:
        """
        Toggle like/unlike for a given recipe by a user.

        Returns:
            True if liked, False if unliked.
        """
        favourite, created = await Favorite.get_or_create(
            user_id=user_id, recipe_id=recipe_id
        )

        if not created:
            # Already liked → unlike it
            await favourite.delete()
            return False
        return True

    async def get_recipe_meta(
        self, recipe_id: UUID, user_id: Optional[UUID] = None
    ) -> dict:
        """
        Fetch recipe metadata like likes, views, comments, shares, and user-specific actions (isLiked, isSaved).

        Args:
            recipe_id (UUID): The ID of the recipe.
            user_id (Optional[UUID]): The ID of the user, if authenticated.

        Returns:
            dict: Metadata dictionary.
        """

        # Aggregate counts
        recipe = await self.recipe_repo.get_or_none(id=recipe_id).prefetch_related(
            "user"
        )
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        like_count = await RecipeLike.filter(recipe_id=recipe_id).count()
        comment_count = await RecipeComment.filter(
            recipe_id=recipe_id, is_deleted=False
        ).count()
        view_count = await RecipeView.filter(recipe_id=recipe_id).count()
        share_count = await ShareRecipe.filter(recipe_id=recipe_id).count()

        # Check if the user follows the recipe's author
        is_following = False

        # Default user-specific flags)
        is_liked = False
        is_saved = False

        # Only check user-specific states if user_id is provided
        if user_id:
            is_liked = await RecipeLike.filter(
                recipe_id=recipe_id, user_id=user_id
            ).exists()
            is_saved = await Favorite.filter(
                recipe_id=recipe_id, user_id=user_id
            ).exists()
            is_following = await Follow.filter(
                follower_id=user_id, following_id=recipe.user.id
            ).exists()

        return {
            "likeCount": like_count,
            "comments": comment_count,
            "views": view_count,
            "shareCount": share_count,
            "isLiked": is_liked,
            "isSaved": is_saved,
            "isFollowing": is_following,
        }

    async def share(
        self, user_id: UUID, recipe_id: UUID, shared_to: str = None, message: str = None
    ) -> bool:
        """
        Create or update a share record for a given recipe.

        If a record already exists for the same user, recipe, and shared_to target,
        the message will be updated.

        Returns:
            True if the share was created or updated successfully.
        """
        share, created = await ShareRecipe.get_or_create(
            user_id=user_id,
            recipe_id=recipe_id,
            shared_to=shared_to,
            defaults={"message": message},
        )

        # If the record exists but message has changed, update it
        if not created and message and share.message != message:
            share.message = message
            await share.save()

        return True

    async def post_comment(
        self, user_id: UUID, recipe_id: UUID, comment: str
    ) -> Union[RecipeComment, None]:
        """
        Post a new top-level comment on a recipe.
        Returns:
            RecipeComment object if created successfully, else None.
        """
        try:
            # Get the recipe with the owner
            recipe = await Recipe.get_or_none(id=recipe_id).prefetch_related("user")
            if not recipe:
                return None

            # Create the comment
            comment_obj = await RecipeComment.create(
                user_id=user_id, recipe_id=recipe_id, content=comment.strip()
            )

            # Notify recipe owner (not self)
            if recipe.user_id != user_id:
                try:
                    notification = await Notification.create(
                        user_id=recipe.user_id,  # recipient
                        actor_id=user_id,  # commenter
                        notification_type="comment",
                        target_object_id=str(recipe.id),
                        target_content_type="comment",
                        thread_id=str(recipe.id),
                        verb=f"commented on your recipe '{recipe.name}'",
                        preview=(comment or "")[:100],
                        second_target_object_id=str(comment_obj.id)
                        if comment_obj
                        else None,
                    )

                    # Try to emit via WebSocket
                    try:
                        from app import notifications_namespace

                        noty = await Notification.filter(
                            id=notification.id
                        ).prefetch_related("user", "actor")

                        await notifications_namespace.trigger_notification({
                            "user_id": str(recipe.user_id),
                            "notifications": noty,
                        })
                    except Exception as emit_error:
                        logger.warning(
                            f"[WebSocket Emit] Notification failed: {emit_error}"
                        )

                except Exception as notify_error:
                    logger.warning(
                        f"[Notification Create] Notification failed: {notify_error}"
                    )

            return comment_obj

        except Exception as e:
            logger.exception("Error posting comment")
            return None

    async def reply_to_comment(
        self, user_id: UUID, recipe_id: UUID, parent_comment_id: int, reply: str
    ) -> Union[RecipeComment, None]:
        """
        Reply to an existing comment on a recipe.
        Notifies the parent comment owner and recipe owner if they are different from the replier.
        """
        try:
            parent = await RecipeComment.get_or_none(
                id=parent_comment_id, recipe_id=recipe_id
            ).prefetch_related("user", "recipe")
            if not parent:
                return None

            recipe = await Recipe.get_or_none(id=recipe_id).prefetch_related("user")
            if not recipe:
                return None

            comment_obj = await RecipeComment.create(
                user_id=user_id,
                recipe_id=recipe_id,
                content=reply.strip(),
                parent_id=parent_comment_id,
            )

            try:
                from app import (
                    notifications_namespace,
                )  # Lazy import to avoid circular import issues

                # Notify parent commenter if not self
                if parent.user_id != user_id:
                    try:
                        parent_notification = await Notification.create(
                            user_id=parent.user_id,
                            actor_id=user_id,
                            notification_type="comment",
                            target_object_id=str(recipe.id),
                            target_content_type="recipecomment",
                            verb=f"replied to your comment on '{recipe.name}'",
                            thread_id=str(parent_comment_id),
                            second_target_object_id=str(parent_comment_id)
                            if parent_comment_id
                            else None,
                            preview=(reply or "")[:100],
                        )
                        noty = await Notification.filter(
                            id=parent_notification.id
                        ).prefetch_related("user", "actor")

                        await notifications_namespace.trigger_notification({
                            "user_id": str(parent.user_id),
                            "notifications": noty,
                        })
                    except Exception as e:
                        logger.warning(
                            f"[Notification: Parent Commenter] Failed to notify: {e}"
                        )

                # Notify recipe owner if not self or already notified
                if recipe.user_id != user_id and recipe.user_id != parent.user_id:
                    try:
                        recipe_owner_notification = await Notification.create(
                            user_id=recipe.user_id,
                            actor_id=user_id,
                            notification_type="comment",
                            target_object_id=str(recipe.id),
                            target_content_type="recipecomment",
                            verb=f"commented on your recipe '{recipe.name}",
                            thread_id=recipe.id,
                            preview=(reply or "")[:100],
                        )
                        noty = await Notification.filter(
                            id=recipe_owner_notification.id
                        ).prefetch_related("user", "actor")

                        await notifications_namespace.trigger_notification({
                            "user_id": str(recipe.user_id),
                            "notifications": noty,
                        })
                    except Exception as e:
                        logger.warning(
                            f"[Notification: Recipe Owner] Failed to notify: {e}"
                        )

            except ImportError as e:
                logger.warning(
                    f"[Notification Import] Failed to import notifications_namespace: {e}"
                )

            return comment_obj

        except Exception as e:
            logger.error(f"[Reply Comment] Error creating reply: {e}")
            return None

    async def edit_comment(
        self, user_id: UUID, comment_id: int, new_content: str
    ) -> Union[RecipeComment, None]:
        """
        Edit an existing comment if it belongs to the user.
        """
        comment = await RecipeComment.get_or_none(id=comment_id, user_id=user_id)
        if not comment:
            return None

        if comment.content.strip() != new_content.strip():
            comment.content = new_content.strip()
            comment.is_edited = True
            await comment.save()

        return comment

    async def delete_comment(self, user_id: UUID, comment_id: int) -> bool:
        """
        Soft delete a comment if it belongs to the user.
        """
        comment = await RecipeComment.get_or_none(id=comment_id, user_id=user_id)
        if not comment:
            return False

        comment.is_deleted = True
        await comment.save()
        return True

    async def delete_recipe(self, user_id: UUID, recipe_id: UUID) -> bool:
        """
        Delete a recipe if it belongs to the user, including steps, ingredients, comments, likes, etc.
        """
        recipe = await self.recipe_repo.get_or_none(
            id=recipe_id, user_id=user_id
        ).prefetch_related("steps__ingredients", "tags", "category")
        if not recipe:
            return False

        # Delete all related ingredients and steps
        for step in recipe.steps:
            await step.ingredients.all().delete()
            await step.delete()

        # Clear M2M fields
        await recipe.tags.clear()
        await recipe.category.clear()

        # Delete related records
        await RecipeComment.filter(recipe_id=recipe_id).delete()
        await RecipeLike.filter(recipe_id=recipe_id).delete()
        await Favorite.filter(recipe_id=recipe_id).delete()
        await ShareRecipe.filter(recipe_id=recipe_id).delete()
        await RecipeView.filter(recipe_id=recipe_id).delete()

        # Finally delete the recipe
        await recipe.delete()
        return True

    async def get_comments(
        self,
        recipe_id: UUID,
        parent: Optional[int] = None,
        user_id: Optional[UUID] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> dict:
        """
        Get recipe comments:
        - If parent is None: top-level comments with 1 reply + reply count
        - If parent is set: fetch full thread in flat structure
        """
        try:
            if parent is None:
                # Step 1: Fetch top-level comments
                top_comments = (
                    await RecipeComment.filter(
                        recipe_id=recipe_id, is_deleted=False, parent_id=None
                    )
                    .prefetch_related("user", "likes")
                    .order_by("-created_at")
                    .offset(offset)
                    .limit(limit)
                )

                # Step 2: Collect comment IDs
                top_ids = [c.id for c in top_comments]

                # Step 3: Fetch replies in batch
                replies_map = {
                    r.parent_id: r
                    for r in await RecipeComment.filter(
                        recipe_id=recipe_id,
                        parent_id__in=top_ids,
                        is_deleted=False,
                    )
                    .order_by("created_at")
                    .prefetch_related("user", "likes")
                }

                # Step 4: Batch fetch user likes for current user
                user_likes_map = {}
                if user_id:
                    user_likes = await CommentLike.filter(
                        user_id=user_id,
                        comment_id__in=top_ids + list(replies_map.keys()),
                    )
                    user_likes_map = {ul.comment_id: ul for ul in user_likes}

                # Step 5: Build response
                result = []
                for comment in top_comments:
                    user_like = user_likes_map.get(comment.id)

                    comment_dict = {
                        "id": comment.id,
                        "content": comment.content,
                        "is_edited": comment.is_edited,
                        "likes": len(comment.likes),
                        "isLiked": bool(user_like),
                        "reacted_emoji": user_like.reaction if user_like else None,
                        "created_at": comment.created_at.isoformat(),
                        "parent_id": comment.parent_id,
                        "attachments": list(comment.attachments)
                        if isinstance(comment.attachments, (list, tuple))
                        else [],
                        "user": {
                            "id": str(comment.user.id),
                            "name": getattr(comment.user, "name", "Unknown"),
                            "profilePic": comment.user.picture_url
                            if comment.user.picture_url.startswith("https://")
                            else f"{BASE_SERVER}/{comment.user.picture_url}",
                        },
                        "replies": [],
                        "replyCount": await RecipeComment.filter(
                            recipe_id=recipe_id, parent_id=comment.id, is_deleted=False
                        ).count(),
                    }

                    # Append first reply if exists
                    reply = replies_map.get(comment.id)
                    if reply:
                        reply_user_like = user_likes_map.get(reply.id)
                        replied_to_name = getattr(comment.user, "name", "")
                        reply_dict = {
                            "id": reply.id,
                            "content": f"@{replied_to_name} {reply.content}",
                            "is_edited": reply.is_edited,
                            "likes": len(reply.likes),
                            "isLiked": bool(reply_user_like),
                            "reacted_emoji": reply_user_like.reaction
                            if reply_user_like
                            else None,
                            "created_at": reply.created_at.isoformat(),
                            "parent_id": reply.parent_id,
                            "attachments": list(reply.attachments)
                            if isinstance(reply.attachments, (list, tuple))
                            else [],
                            "user": {
                                "id": str(reply.user.id),
                                "name": getattr(reply.user, "name", "Unknown"),
                                "profilePic": reply.user.picture_url
                                if reply.user.picture_url.startswith("https://")
                                else f"{BASE_SERVER}/{reply.user.picture_url}",
                            },
                        }
                        comment_dict["replies"].append(reply_dict)

                    result.append(comment_dict)

                total = await RecipeComment.filter(
                    recipe_id=recipe_id, is_deleted=False, parent_id=None
                ).count()

                return {
                    "comments": result,
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                }

            else:
                # Flat reply thread (recursive)
                logger.info("Fetching replies for parent: %s", parent)

                all_replies = (
                    await RecipeComment.filter(recipe_id=recipe_id, is_deleted=False)
                    .prefetch_related("user", "likes")
                    .order_by("created_at")
                )

                parent_map = {c.id: c.parent_id for c in all_replies}
                user_map = {
                    c.id: getattr(c.user, "name", "Unknown") for c in all_replies
                }

                def is_descendant(child_id):
                    pid = parent_map.get(child_id)
                    while pid:
                        if pid == parent:
                            return True
                        pid = parent_map.get(pid)
                    return False

                filtered_replies = [
                    c for c in all_replies if c.id != parent and is_descendant(c.id)
                ]
                paginated_replies = filtered_replies[offset : offset + limit]

                # Batch user likes
                reply_ids = [c.id for c in paginated_replies]
                reply_likes = (
                    await CommentLike.filter(user_id=user_id, comment_id__in=reply_ids)
                    if user_id
                    else []
                )
                reply_likes_map = {ul.comment_id: ul for ul in reply_likes}

                replies = []
                for c in paginated_replies:
                    user_like = reply_likes_map.get(c.id)
                    replied_to_name = user_map.get(parent_map.get(c.id))
                    prefix = f"@{replied_to_name} " if replied_to_name else ""

                    replies.append({
                        "id": c.id,
                        "content": f"{prefix}{c.content}",
                        "is_edited": c.is_edited,
                        "likes": len(c.likes),
                        "isLiked": bool(user_like),
                        "reacted_emoji": user_like.reaction if user_like else None,
                        "created_at": c.created_at.isoformat(),
                        "parent_id": c.parent_id,
                        "attachments": list(c.attachments)
                        if isinstance(c.attachments, (list, tuple))
                        else [],
                        "user": {
                            "id": str(c.user.id),
                            "name": getattr(c.user, "name", "Unknown"),
                            "profilePic": c.user.picture_url
                            if c.user.picture_url.startswith("https://")
                            else f"{BASE_SERVER}/{c.user.picture_url}",
                        },
                    })

                return {
                    "replies": replies,
                    "total": len(filtered_replies),
                    "limit": limit,
                    "offset": offset,
                }

        except Exception as e:
            logger.exception("Error in get_comments: %s", str(e))
            return {"error": "An unexpected error occurred."}

    async def like_unlike_comment(
        self,
        user_id: UUID,
        recipe_id: UUID,
        comment_id: int,
        is_liked: bool,
        reaction: dict,
    ) -> bool:
        """
        Toggle like/unlike for a comment with optional emoji reaction.

        Args:
            user_id (UUID): ID of the user liking/unliking.
            recipe_id (UUID): ID of the recipe the comment belongs to.
            comment_id (int): ID of the comment.
            is_liked (bool): Whether the comment is being liked or unliked.
            reaction (dict): Emoji or reaction data.

        Returns:
            bool: True if liked or reaction applied, False if unliked or removed.
        """
        try:
            like, created = await CommentLike.get_or_create(
                user_id=user_id, comment_id=comment_id, defaults={"reaction": reaction}
            )

            if not created:
                # Update reaction if changed
                if is_liked:
                    await like.update_from_dict({"reaction": reaction}).save()
                    return True

                # Unlike and remove if no reaction
                if not is_liked:
                    await like.delete()

                    await Notification.filter(
                        actor_id=user_id,
                        target_object_id=str(comment_id),
                        target_content_type="reacted",
                        thread_id=recipe_id,
                    ).delete()

                    return False

                # If unliking but reaction exists, just update
                await like.update_from_dict({"reaction": reaction}).save()
                return True

            recipe = await Recipe.get_or_none(id=recipe_id).prefetch_related("user")
            if not recipe or not recipe.user:
                logger.error(
                    f"[Like/Unlike] Recipe or user not found for ID {recipe_id}"
                )
                return True

            from app import notifications_namespace

            rep_comment = await RecipeComment.get_or_none(
                id=comment_id
            ).prefetch_related("user")
            logger.info("sending nitificaiton to %s", rep_comment.user.username)

            if rep_comment.user.id != user_id:
                try:
                    logger.info("sending nitificaiton to %s", rep_comment.user.username)
                    notification = await Notification.create(
                        user_id=rep_comment.user.id,
                        actor_id=user_id,
                        notification_type="like",
                        target_object_id=str(recipe.id),
                        target_content_type="reacted",
                        verb=f"reacted to your comment on '{recipe.name[:100]}'",
                        preview=recipe.name[:100],
                        thread_id=str(recipe.id),
                    )

                    noty = await Notification.filter(
                        id=notification.id
                    ).prefetch_related("user", "actor")

                    await notifications_namespace.trigger_notification({
                        "user_id": str(rep_comment.user.id),
                        "notifications": noty,
                    })
                except Exception as e:
                    logger.warning(f"[Notification Create] Failed to send: {e}")

            return True

        except Exception as e:
            logger.error(f"[Like/Unlike] Unexpected error: {e}")
            return False

    async def get_viewers(
        self,
        recipe_id: UUID,
        user_id: Optional[UUID],
        offset: int = 0,
        limit: int = 10,
    ) -> dict:
        """
        Retrieve viewers of a specific recipe, including user details and follow status.
        """
        # Fetch viewers for the given recipe
        viewers = (
            await RecipeView.filter(recipe_id=recipe_id)
            .offset(offset)
            .limit(limit)
            .prefetch_related("user")
        )

        print(viewers)

        users = [view.user for view in viewers if view.user]
        user_ids = [user.id for user in users]

        # Determine which users are followed by the requesting user
        following_ids = set()
        if user_id:
            following_ids = set(
                await Follow.filter(
                    follower_id=user_id, following_id__in=user_ids
                ).values_list("following_id", flat=True)
            )

        result = [
            {
                "id": str(user.id),
                "name": getattr(user, "name", "Unknown"),
                "username": getattr(user, "username", "unknown"),
                "isChef": user.is_chef,
                "avatar": (
                    user.picture_url
                    if user.picture_url and user.picture_url.startswith("https://")
                    else f"{BASE_SERVER}/{user.picture_url}"
                    if user.picture_url
                    else ""
                ),
                "isFollowing": user.id in following_ids,
            }
            for user in users
        ]

        return {
            "viewers": result,
            "offset": offset,
            "limit": limit,
            "count": len(result),
        }

    async def get_likes(
        self,
        recipe_id: UUID,
        user_id: Optional[UUID],
        offset: int = 0,
        limit: int = 10,
    ) -> dict:
        """
        Retrieve viewers of a specific recipe, including user details and follow status.
        """
        # Fetch viewers for the given recipe
        viewers = (
            await RecipeLike.filter(recipe_id=recipe_id)
            .offset(offset)
            .limit(limit)
            .prefetch_related("user")
        )

        print(viewers)

        users = [view.user for view in viewers if view.user]
        user_ids = [user.id for user in users]

        # Determine which users are followed by the requesting user
        following_ids = set()
        if user_id:
            following_ids = set(
                await Follow.filter(
                    follower_id=user_id, following_id__in=user_ids
                ).values_list("following_id", flat=True)
            )

        result = [
            {
                "id": str(user.id),
                "name": getattr(user, "name", "Unknown"),
                "username": getattr(user, "username", "unknown"),
                "isChef": user.is_chef,
                "avatar": (
                    user.picture_url
                    if user.picture_url and user.picture_url.startswith("https://")
                    else f"{BASE_SERVER}/{user.picture_url}"
                    if user.picture_url
                    else ""
                ),
                "isFollowing": user.id in following_ids,
            }
            for user in users
        ]

        return {
            "likers": result,
            "offset": offset,
            "limit": limit,
            "count": len(result),
        }

    async def get_all_recipes(self, user_id: UUID) -> dict:
        recipes = await self.recipe_repo.filter(user_id=user_id).order_by("-updated_at")

        r_recipes = [
            {
                "id": str(r.id),
                "image": f"{BASE_SERVER}/{r.cover_image_url}" or "",
                "name": r.name,
                "created_at": r.updated_at.isoformat() or r.created_at.isoformat(),
            }
            for r in recipes
        ]

          
        return {"all_recipes": r_recipes}

    async def get_general_recipes_stats(self, user_id: UUID) -> dict:
        recipes = await self.recipe_repo.filter(user_id=user_id)

        now = datetime.now(timezone.utc)
        last_7_days = now - timedelta(days=7)
        prev_7_days = now - timedelta(days=14)

        total_views = total_engagements = total_active_time = 0
        recent_views = recent_engagements = recent_active_time = 0
        previous_views = previous_engagements = previous_active_time = 0

        recipe_views = []
        labels = []
        recipe_colors = []
        for recipe in recipes:
            # All-time views
            views = await RecipeView.filter(recipe=recipe)
            total_views += len(views)
            total_active_time += sum(v.active_time for v in views)
            total_engagements += len(views)
            labels.append(recipe.name[:10])
            recipe_colors.append(recipe.theme_color if hasattr(recipe, "theme_color") else "#ccc")
            recipe_views.append(len(views))

            # Views in last 7 days
            recent_views_qs = await RecipeView.filter(
                recipe=recipe, viewed_on__gte=last_7_days
            )
            recent_views += len(recent_views_qs)
            recent_active_time += sum(v.active_time for v in recent_views_qs)
            recent_engagements += len(recent_views_qs)

            # Views in previous 7 days
            prev_views_qs = await RecipeView.filter(
                recipe=recipe, viewed_on__gte=prev_7_days, viewed_on__lt=last_7_days
            )
            previous_views += len(prev_views_qs)
            previous_active_time += sum(v.active_time for v in prev_views_qs)
            previous_engagements += len(prev_views_qs)

            # All-time likes/shares/favorites
            total_engagements += await RecipeLike.filter(recipe=recipe).count()
            total_engagements += await ShareRecipe.filter(recipe=recipe).count()
            total_engagements += await Favorite.filter(recipe=recipe).count()

            # Replace the created_at fields below based on actual model fields
            recent_engagements += await RecipeLike.filter(
                recipe=recipe, created_at__gte=last_7_days
            ).count()
            recent_engagements += await ShareRecipe.filter(
                recipe=recipe, created_at__gte=last_7_days
            ).count()
            recent_engagements += await Favorite.filter(
                recipe=recipe, added_at__gte=last_7_days
            ).count()

            previous_engagements += await RecipeLike.filter(
                recipe=recipe, created_at__gte=prev_7_days, created_at__lt=last_7_days
            ).count()
            previous_engagements += await ShareRecipe.filter(
                recipe=recipe, created_at__gte=prev_7_days, created_at__lt=last_7_days
            ).count()
            previous_engagements += await Favorite.filter(
                recipe=recipe, added_at__gte=prev_7_days, added_at__lt=last_7_days
            ).count()

        def calc_change(current, previous):
            diff = current - previous
            percent = (diff / previous * 100) if previous else 100 if current > 0 else 0
            return round(diff), round(percent, 2)

        view_change, view_percent = calc_change(recent_views, previous_views)
        engage_change, engage_percent = calc_change(
            recent_engagements, previous_engagements
        )
        active_change, active_percent = calc_change(
            recent_active_time, previous_active_time
        )

        eng = [
            {
                "label": "Total Views",
                "value": str(total_views),
                "change": view_change,
                "percent": view_percent,
                "icon": "pi pi-eye",
            },
            {
                "label": "Total Engagements",
                "value": str(total_engagements),
                "change": engage_change,
                "percent": engage_percent,
                "icon": "pi pi-heart",
            },
            {
                "label": "Total ActiveTime",
                "value": str(total_active_time),
                "change": active_change,
                "percent": active_percent,
                "icon": "pi pi-users",
            },
        ]
        return {
            "stats": eng,
            "stats_graph_meta": {
                "data": recipe_views,
                "colors": recipe_colors,
                "labels": labels,
            },
        }

    async def get_recipe_report(self, user_id: UUID, recipe_id: UUID) -> dict:
        recipe = await self.recipe_repo.filter(id=recipe_id).first()
        if not recipe:
            return {}

        now = datetime.now(timezone.utc)
        last_7_days = now - timedelta(days=7)

        # Likes
        total_likes = await RecipeLike.filter(recipe_id=recipe_id).count()
        likes_last_7_days = await RecipeLike.filter(
            recipe_id=recipe_id, created_at__gte=last_7_days
        ).count()
        likes_change = (likes_last_7_days / total_likes * 100) if total_likes else 0

        # Comments
        total_comments = await RecipeComment.filter(
            recipe_id=recipe_id, is_deleted=False
        ).count()
        comments_last_7_days = await RecipeComment.filter(
            recipe_id=recipe_id, is_deleted=False, created_at__gte=last_7_days
        ).count()
        comments_change = (
            (comments_last_7_days / total_comments * 100) if total_comments else 0
        )

        # Views and Active Time
        views = await RecipeView.filter(recipe_id=recipe_id)
        total_views = len(views)
        active_time = sum(view.active_time for view in views)
        views_last_7_days = await RecipeView.filter(
            recipe_id=recipe_id, viewed_on__gte=last_7_days
        ).count()
        views_change = (views_last_7_days / total_views * 100) if total_views else 0

        # Shares
        total_shares = await ShareRecipe.filter(recipe_id=recipe_id).count()
        shares_last_7_days = await ShareRecipe.filter(
            recipe_id=recipe_id, created_at__gte=last_7_days
        ).count()
        shares_change = (shares_last_7_days / total_shares * 100) if total_shares else 0

        # Saves
        total_saves = await Favorite.filter(recipe_id=recipe_id).count()
        saves_last_7_days = await Favorite.filter(
            recipe_id=recipe_id, added_at__gte=last_7_days
        ).count()
        saves_change = (saves_last_7_days / total_saves * 100) if total_saves else 0

        # Completion Rate (random for now, can be refined)
        completion_rate = random.randint(87, 97)

        return {
            "id": str(recipe.id),
            "name": recipe.name,
            "image": f"{BASE_SERVER}/{recipe.cover_image_url}" or "",
            "created_at": recipe.updated_at.isoformat()
            or recipe.created_at.isoformat(),
            "views": total_views,
            "views_change": round(views_change, 2),
            "likes": total_likes,
            "likes_change": round(likes_change, 2),
            "comments": total_comments,
            "comments_change": round(comments_change, 2),
            "shares": total_shares,
            "shares_change": round(shares_change, 2),
            "saves": total_saves,
            "saves_change": round(saves_change, 2),
            "active_time": active_time,
            "completion_rate": completion_rate,
        }

    async def get_recipe_chart_report(
        self, user_id: UUID, recipe_id: UUID, days: int = 30
    ) -> dict:
        now = datetime.now(timezone.utc)
        last_7_days = now - timedelta(days=days)

        # Last 7 days stats
        likes = await RecipeLike.filter(
            recipe_id=recipe_id, created_at__gte=last_7_days
        ).count()
        comments = await RecipeComment.filter(
            recipe_id=recipe_id, is_deleted=False, created_at__gte=last_7_days
        ).count()
        views_qs = await RecipeView.filter(
            recipe_id=recipe_id, viewed_on__gte=last_7_days
        )
        shares = await ShareRecipe.filter(
            recipe_id=recipe_id, created_at__gte=last_7_days
        ).count()
        saves = await Favorite.filter(
            recipe_id=recipe_id, added_at__gte=last_7_days
        ).count()

        active_time = sum(view.active_time for view in views_qs)

        return {
            "labels": ["Likes", "Comments", "Views", "Shares", "Saves", "Active Time"],
            "datasets": [
                {
                    "label": f"Recipe Report (Last {days} Days)",
                    "data": [
                        likes,
                        comments,
                        len(views_qs),
                        shares,
                        saves,
                        active_time,
                    ],
                    "backgroundColor": [
                        "rgba(249, 115, 22, 0.2)",
                        "rgba(6, 182, 212, 0.2)",
                        "rgba(107, 114, 128, 0.2)",
                        "rgba(139, 92, 246, 0.2)",
                        "rgba(34, 197, 94, 0.2)",
                        "rgba(239, 68, 68, 0.2)",
                    ],
                    "borderColor": [
                        "rgb(249, 115, 22)",
                        "rgb(6, 182, 212)",
                        "rgb(107, 114, 128)",
                        "rgb(139, 92, 246)",
                        "rgb(34, 197, 94)",
                        "rgb(239, 68, 68)",
                    ],
                    "borderWidth": 1,
                }
            ],
        }

    # Helper to generate time buckets
    def generate_time_labels(self, recipe_created_at, now):
        delta = now - recipe_created_at
        if delta.days >= 365:
            return [
                now - timedelta(days=30 * i) for i in reversed(range(12))
            ], "monthly"
        elif delta.days >= 90:
            return [now - timedelta(days=10 * i) for i in reversed(range(9))], "10days"
        else:
            return [now - timedelta(days=i) for i in reversed(range(7))], "daily"

    async def get_dynamic_recipe_chart(self, user_id: UUID, recipe_id: UUID):
        now = datetime.now(timezone.utc)
        recipe = await self.recipe_repo.filter(id=recipe_id).first()
        if not recipe:
            return {}

        labels_raw, mode = self.generate_time_labels(
            recipe.created_at or recipe.updated_at, now
        )
        labels = [
            dt.strftime("%b %d") if mode == "daily" else dt.strftime("%b")
            for dt in labels_raw
        ]

        # Bucketed results
        data_map = defaultdict(lambda: [0] * len(labels))

        # Fetch events
        likes = await RecipeLike.filter(recipe_id=recipe_id).all()
        comments = await RecipeComment.filter(
            recipe_id=recipe_id, is_deleted=False
        ).all()
        views = await RecipeView.filter(recipe_id=recipe_id).all()
        shares = await ShareRecipe.filter(recipe_id=recipe_id).all()
        saves = await Favorite.filter(recipe_id=recipe_id).all()

        def distribute(entries, attr_name):
            for entry in entries:
                time = getattr(entry, attr_name)
                for i, label_date in enumerate(labels_raw):
                    end = label_date + timedelta(
                        days=10 if mode == "10days" else 1 if mode == "daily" else 30
                    )
                    if label_date <= time < end:
                        data_map[attr_name][i] += 1
                        break

        distribute(likes, "created_at")
        distribute(comments, "created_at")
        distribute(views, "viewed_on")
        distribute(shares, "created_at")
        distribute(saves, "added_at")

        active_time_data = [0] * len(labels)
        for view in views:
            for i, label_date in enumerate(labels_raw):
                end = label_date + timedelta(
                    days=10 if mode == "10days" else 1 if mode == "daily" else 30
                )
                if label_date <= view.viewed_on < end:
                    active_time_data[i] += view.active_time
                    break

        data_map["active_time"] = active_time_data

        # Prepare dataset
        base_colors = {
            "created_at": "rgb(249, 115, 22)",
            "viewed_on": "rgb(107, 114, 128)",
            "added_at": "rgb(34, 197, 94)",
            "active_time": "rgb(239, 68, 68)",
        }

        label_map = {
            "created_at": "Likes / Comments / Shares",
            "viewed_on": "Views",
            "added_at": "Saves",
            "active_time": "Active Time",
        }

        datasets = []
        for key, data in data_map.items():
            color = base_colors.get(key, "rgb(6, 182, 212)")
            datasets.append({
                "label": label_map.get(key, key.title()),
                "fill": False,
                "borderColor": color,
                "tension": 0.4,
                "data": data,
            })

        # Optional: compare with best-performing recipe
        top_recipe = await self.recipe_repo.filter(user_id=user_id).first()
        if top_recipe and str(top_recipe.id) != str(recipe_id):
            # Add dotted line for best recipe views as example
            best_views = await RecipeView.filter(recipe_id=top_recipe.id).count()
            datasets.append({
                "label": f"Best Recipe (Avg Views)",
                "fill": False,
                "borderColor": "rgba(100,100,255,0.5)",
                "borderDash": [5, 5],
                "tension": 0.4,
                "data": [best_views // len(labels)] * len(labels),
            })

        return {"labels": labels, "datasets": datasets}


# const recipes = [
#     {
#         id: 0,
#         title: "General Overview",
#         description: "Aggregate analytics across all your recipes",
#         name: "Dashboard",
#         image: "https://images.unsplash.com/photo-1490645935967-10de6ba17061",
#     },
#     {
#         id: 1uigoigvv,
#         title: "Spicy Garlic Shrimp Pasta",
#         description: "A delicious pasta dish with a spicy garlic kick and fresh shrimp",
#         name: "Pasta",
#         image: "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb",
#         views: 12543,
#         views_change: 12.5,
#         likes: 892,
#         likes_change: 8.2,
#         shares: 324,
#         shares_change: 5.7,
#         saves: 567,
#         saves_change: 15.3,
#         active_time: 78,
#         completion_rate: 65
#     },
#     {
#         id: 2vkjvkjvy,
#         title: "Avocado Toast",
#         description: "Healthy breakfast with creamy avocado and poached eggs",
#         name: "Breakfast",
#         image: "https://images.unsplash.com/photo-1511690656952-34342bb7c2f2",
#         views: 8765,
#         views_change: -3.2,
#         likes: 654,
#         likes_change: 2.1,
#         shares: 198,
#         shares_change: -1.5,
#         saves: 432,
#         saves_change: 7.8,
#         active_time: 65,
#         completion_rate: 72
#     },
#     {
#         id: uiuhuiogygy,
#         title: "Chocolate Lava Cake",
#         description: "Decadent chocolate dessert with a molten center",
#         name: "Dessert",
#         image: "https://images.unsplash.com/photo-1571115177098-24ec42ed204d",
#         views: 15321,
#         views_change: 18.7,
#         likes: 1243,
#         likes_change: 22.4,
#         shares: 512,
#         shares_change: 14.6,
#         saves: 876,
#         saves_change: 19.2,
#         active_time: 82,
#         completion_rate: 58
#     }
# ];
