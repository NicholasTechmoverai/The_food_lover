from models import Recipe, RecipeStep, Tag, Category,Ingredient,RecipeLike,RecipeComment,ShareRecipe,Favorite,RecipeView
from reusables.main import sanitizeContents ,save_base64_image,sanitize_name
from uuid import  UUID
from tortoise.expressions import Q
from typing import Tuple
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException
from typing import Any
import os
from pydantic import BaseModel, Field
from typing import List, Optional, Union

from config import Config,BASE_SERVER



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
    category: Optional[str] = None
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

    async def create_or_update_recipe(self, data: RecipeRequest, user_id: UUID,user_name):
        upload_path = os.path.join( Config.CHEF_PATH, await sanitize_name(user_name))
        
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
            recipe.cover_image_url = await save_base64_image(data.recipeCover.image, upload_path)
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
                cover_image_url=await save_base64_image(data.recipeCover.image, upload_path),
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
                image_url=await save_base64_image(step_data.image,upload_path),
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
                "image": F"{BASE_SERVER}/{r.cover_image_url}",
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

        return {"recipes":result,
                "limit":limit,
                "offset":offset
                }

    async def get_recipe_by_id(self, name: str, recipe_id: UUID, user_id: UUID = None) -> Tuple[dict[str, Any], dict[str, Any]]:
        recipe = await self.recipe_repo.get_or_none(id=recipe_id).prefetch_related(
            "tags", "category", "steps__ingredients", "user"
        )

        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        def minutes_to_time(total: int):
            return {"hr": total // 60, "min": total % 60}

        recipe_cover = {
            "id": str(recipe.id),
            "recipeName": recipe.name,
            "repiceColor": recipe.theme_color,
            "image": f"{BASE_SERVER}/{recipe.cover_image_url}",
            "tags": [tag.name for tag in recipe.tags],
            "cookTime": minutes_to_time(recipe.cook_time_minutes),
            "description": recipe.description,
            "cuisine": {
                "name": recipe.cuisine,
                "region": "East Africa",  # Optional: adjust based on actual DB info
            },
            "complexityLevel": {
                "name": recipe.difficulty_level.capitalize(),
                "value": {"Easy": 1, "Medium": 2, "Hard": 3}.get(recipe.difficulty_level.capitalize(), 1),
            },
            "category": [cat.name for cat in recipe.category],
            "user": {
                "name": getattr(recipe.user, "name", "Unknown"),
                "profilePic": getattr(recipe.user, "profile_pic", ""),
                "id": str(recipe.user.id),
                "totalRecipes": await self.recipe_repo.filter(user=recipe.user).count(),
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
                {
                    "name": ing.name,
                    "amount": ing.quantity,
                    "unit": ing.unit
                }
                for ing in step.ingredients
            ]

            step_entry = {
                "no": step.step_number,
                "timeRequired": minutes_to_time(step.cook_time_minutes or 0),
                "tempRequired": step.temperature_celsius,
                "instructions": step.description,
                "image": f"{BASE_SERVER}/{step.image_url}",
                "videoUrl": step.video_url,
                "ingredientsUsed": ingredients_used,
            }

            recipe_steps["steps"].append(step_entry)

        return recipe_cover, recipe_steps
    
    async def like_unlike(self, user_id: UUID, recipe_id: UUID) -> bool:
        """
        Toggle like/unlike for a given recipe by a user.
        
        Returns:
            True if liked, False if unliked.
        """
        like, created = await RecipeLike.get_or_create(user_id=user_id, recipe_id=recipe_id)

        if not created:
            # Already liked → unlike it
            await like.delete()
            return False

        # Liked just now
        #TODO:send notifications to chef
        return True
    async def like_unlike_favourite(self, user_id: UUID, recipe_id: UUID) -> bool:
        """
        Toggle like/unlike for a given recipe by a user.
        
        Returns:
            True if liked, False if unliked.
        """
        favourite, created = await Favorite.get_or_create(user_id=user_id, recipe_id=recipe_id)

        if not created:
            # Already liked → unlike it
            await favourite.delete()
            return False
        return True
    
    async def get_recipe_meta(self, recipe_id: UUID, user_id: Optional[UUID] = None) -> dict:
        """
        Fetch recipe metadata like likes, views, comments, shares, and user-specific actions (isLiked, isSaved).

        Args:
            recipe_id (UUID): The ID of the recipe.
            user_id (Optional[UUID]): The ID of the user, if authenticated.

        Returns:
            dict: Metadata dictionary.
        """

        # Aggregate counts
        like_count = await RecipeLike.filter(recipe_id=recipe_id).count()
        comment_count = await RecipeComment.filter(recipe_id=recipe_id, is_deleted=False).count()
        view_count = await Favorite.filter(recipe_id=recipe_id).count()
        share_count = await ShareRecipe.filter(recipe_id=recipe_id).count()

        # Default user-specific flags
        is_liked = False
        is_saved = False

        # Only check user-specific states if user_id is provided
        if user_id:
            is_liked = await RecipeLike.filter(recipe_id=recipe_id, user_id=user_id).exists()
            is_saved = await Favorite.filter(recipe_id=recipe_id, user_id=user_id).exists()

        return {
            "likeCount": like_count,
            "comments": comment_count,
            "views": view_count,
            "shareCount": share_count,
            "isLiked": is_liked,
            "isSaved": is_saved
        }        
    async def share(
        self,
        user_id: UUID,
        recipe_id: UUID,
        shared_to: str = None,
        message: str = None
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
            defaults={"message": message}
        )

        # If the record exists but message has changed, update it
        if not created and message and share.message != message:
            share.message = message
            await share.save()

        return True
    
    async def post_comment(self, user_id: UUID, recipe_id: UUID, comment: str) -> Union[RecipeComment, None]:
        """
        Post a new top-level comment on a recipe.

        Returns:
            RecipeComment object if created successfully, else None.
        """
        try:
            comment_obj = await RecipeComment.create(
                user_id=user_id,
                recipe_id=recipe_id,
                content=comment.strip()
            )
            # TODO: Notify recipe author
            return comment_obj
        except Exception as e:
            print("Error posting comment:", e)
            return None
    async def reply_to_comment(self, user_id: UUID, recipe_id: UUID, parent_comment_id: int, reply: str) -> Union[RecipeComment, None]:
        """
        Reply to an existing comment on a recipe.
        """
        try:
            parent = await RecipeComment.get_or_none(id=parent_comment_id, recipe_id=recipe_id)
            if not parent:
                return None  # parent doesn't exist or wrong recipe

            comment_obj = await RecipeComment.create(
                user_id=user_id,
                recipe_id=recipe_id,
                content=reply.strip(),
                parent_id=parent_comment_id
            )
            # TODO: Optionally notify the parent commenter
            return comment_obj
        except Exception as e:
            print("Error posting reply:", e)
            return None
        
    async def edit_comment(self, user_id: UUID, comment_id: int, new_content: str) -> Union[RecipeComment, None]:
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
        recipe = await self.recipe_repo.get_or_none(id=recipe_id, user_id=user_id).prefetch_related(
            "steps__ingredients", "tags", "category"
        )
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

        # Finally delete the recipe
        await recipe.delete()
        return True

    async def get_comments(self, recipe_id: UUID, parent: Optional[int] = None, limit: int = 10, offset: int = 0) -> dict:
        """
        Get recipe comments:
        - If parent is None: top-level comments with 1 reply + reply count
        - If parent is set: fetch full thread in flat structure
        """

        try:
            print("recipe_id received:", recipe_id)
            if parent is None:
                print("parent is none")

                # Fetch top-level comments
                top_comments = await RecipeComment.filter(
                    recipe_id=recipe_id,
                    is_deleted=False,
                    parent_id=None
                ).prefetch_related("user").order_by("-created_at").offset(offset).limit(limit)

                result = []

                print("result", [f"{c.user.name}: {c.content}" for c in top_comments])

                for comment in top_comments:
                    print("this comment", f"{comment.user.name}: {comment.content}")

                    # First reply (if exists)
                    first_reply = await RecipeComment.filter(
                        recipe_id=recipe_id,
                        parent_id=comment.id,
                        is_deleted=False
                    ).prefetch_related("user").order_by("created_at").first()

                    # Count of all replies
                    reply_count = await RecipeComment.filter(
                        recipe_id=recipe_id,
                        parent_id=comment.id,
                        is_deleted=False
                    ).count()

                    comment_dict = {
                        "id": comment.id,
                        "content": comment.content,
                        "is_edited": comment.is_edited,
                        "likes": 0,
                        "created_at": comment.created_at.isoformat(),
                        "parent_id": comment.parent_id,
                        "attachments": list(comment.attachments) if isinstance(comment.attachments, (list, tuple)) else [],
                        "user": {
                            "id": str(comment.user.id),
                            "name": getattr(comment.user, "name", "Unknown"),
                            "profilePic": getattr(comment.user, "profile_pic", "")
                        },
                        "replies": [],
                        "replyCount": reply_count
                    }

                    if first_reply:
                        replied_to_name = getattr(comment.user, "name", "")
                        reply_dict = {
                            "id": first_reply.id,
                            "content": f"@{replied_to_name} {first_reply.content}",
                            "is_edited": first_reply.is_edited,
                            "likes": 0,
                            "created_at": first_reply.created_at.isoformat(),
                            "parent_id": first_reply.parent_id,
                            "attachments": list(first_reply.attachments) if isinstance(first_reply.attachments, (list, tuple)) else [],
                            "user": {
                                "id": str(first_reply.user.id),
                                "name": getattr(first_reply.user, "name", "Unknown"),
                                "profilePic": getattr(first_reply.user, "profile_pic", "")
                            }
                        }
                        comment_dict["replies"].append(reply_dict)

                    result.append(comment_dict)

                total = await RecipeComment.filter(
                    recipe_id=recipe_id,
                    is_deleted=False,
                    parent_id=None
                ).count()

                return {
                    "comments": result,
                    "total": total,
                    "limit": limit,
                    "offset": offset
                }

            else:
                print("Fetching replies for parent:", parent)

                all_replies = await RecipeComment.filter(
                    recipe_id=recipe_id,
                    is_deleted=False
                ).prefetch_related("user").order_by("created_at")

                parent_map = {}
                user_map = {}

                for c in all_replies:
                    parent_map[c.id] = c.parent_id
                    user_map[c.id] = getattr(c.user, "name", "Unknown")

                def is_descendant(child_id):
                    """Check if comment is a descendant of the parent"""
                    pid = parent_map.get(child_id)
                    while pid:
                        if pid == parent:
                            return True
                        pid = parent_map.get(pid)
                    return False

                # Filter out actual descendants (excluding the parent itself)
                filtered_replies = [c for c in all_replies if c.id != parent and is_descendant(c.id)]

                total = len(filtered_replies)  # Total replies before pagination

                # Apply pagination
                paginated_replies = filtered_replies[offset:offset + limit]

                replies = []
                for c in paginated_replies:
                    replied_to_name = user_map.get(parent_map.get(c.id))
                    prefix = f"@{replied_to_name} " if replied_to_name else ""
                    replies.append({
                        "id": c.id,
                        "content": f"{prefix}{c.content}",
                        "is_edited": c.is_edited,
                        "likes": 0,
                        "created_at": c.created_at.isoformat(),
                        "parent_id": c.parent_id,
                        "attachments": list(c.attachments) if isinstance(c.attachments, (list, tuple)) else [],
                        "user": {
                            "id": str(c.user.id),
                            "name": getattr(c.user, "name", "Unknown"),
                            "profilePic": getattr(c.user, "profile_pic", "")
                        }
                    })

                return {
                    "replies": replies,
                    "total": total,
                    "limit": limit,
                    "offset": offset
                }


        except Exception as e:
            print("Error in get_comments:", str(e))
            return {"error": "An unexpected error occurred."}


#  {
#         id: 1,
#         content: 'This is a great recipe! I tried it with coconut milk and it was amazing. 😍',
#         is_edited: false,
#         likes: 5,
#         parent_id: null,
#         created_at: new Date(),
#         user: {
#             id: 456,
#             name: 'Jane Doe',
#             profilePic: defaultAvatar,
#         },
#         replies: [
#             {
#                 id: 2,
#                 content: '@Jane Doe I\'ll definitely try that! Thanks Jane!',
#                 is_edited: true,
#                 likes: 2,
#                 parent_id: 1,
#                 created_at: new Date(),
#                 user: {
#                     id: 789,
#                     name: 'John Smith',
#                     profilePic: defaultAvatar,
#                 },
#             },
#             {
#                 id: 3,
#                 content: 'Coconut milk is a great alternative! Did you use full-fat or light?',
#                 is_edited: false,
#                 likes: 0,
#                 parent_id: 1,
#                 created_at: new Date(Date.now() - 3600000),
#                 user: {
#                     id: 101,
#                     name: 'Alex Johnson',
#                     profilePic: defaultAvatar,
#                 },
#             },
#         ],
#     },
#     {
#         id: 4,
#         content: 'Has anyone tried doubling the spices? I wonder if it would be too strong.',
#         is_edited: false,
#         likes: 1,
#         parent_id: null,
#         created_at: new Date(Date.now() - 86400000),
#         user: {
#             id: 112,
#             name: 'Sam Wilson',
#             profilePic: defaultAvatar,
#         },
#         replies: [],
#         attachments: [
#             {
#                 name: 'recipe-variation.pdf',
#                 url: '#',
#                 type: 'file'
#             }
#         ]
#     },