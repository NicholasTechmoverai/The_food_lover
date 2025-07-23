from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List
import asyncio
from fastapi import Query

from .auth import get_current_user,AuthError
from utils.limiter import limiter  
from utils.recipes import RecipeService,RecipeRequest

from tortoise.expressions import Q
from uuid import UUID
from models import User as Users
from typing import Optional
from pydantic import BaseModel
recipe_router = APIRouter()




@recipe_router.post("/recipes")
@limiter.limit("30/min")
async def create_recipe(
    data: RecipeRequest,
    request: Request,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
 
    if not user.is_chef:
        raise HTTPException(status_code=403, detail="Only chefs can submit recipes")

   
    recipe = await service.create_or_update_recipe(data, user.id,user.name)

    return {
        "message": "Recipe processed successfully",
        "user": user.name,
        "recipeName": data.recipeCover.recipeName,
        "recipeId": str(recipe.id)  
    }




class RecipeFilterRequest(BaseModel):
    limit: int = 10
    offset: int = 0
    public_only: bool = True
    user_id: Optional[str] = None
    recipe_name: Optional[str] = None
    category: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    cuisine: Optional[str] = None
    saved: Optional[bool] = False

@recipe_router.post("/recipes/get")
async def fetch_recipe(
    request_data: RecipeFilterRequest,
    request: Request,
    service: RecipeService = Depends()
):
    try:
        print("recipes in", request_data.category, request_data.tags)

        recipes = await service.list_recipes(
            public_only=request_data.public_only,
            limit=request_data.limit,
            offset=request_data.offset,
            user_id=request_data.user_id,
            name=request_data.recipe_name,
            category=request_data.category,
            cuisine=request_data.cuisine,
            tags=request_data.tags,
            saved=request_data.saved
        )
        return recipes

    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))

@recipe_router.get("/recipes/{name}/{id}")
@limiter.limit("30/min")
async def fetch_recipe_by_id(
    request: Request,
    name: str,
    id: UUID,
    public_only: bool = True,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
    """
    Fetch a specific recipe by its name and UUID.
    Rate-limited to 30 requests per minute.
    """
    try:
        cover, steps = await service.get_recipe_by_id( name, id,user.id)
        return {
            "cover": cover,
            "steps": steps
        }
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch recipe.")
    
    
    
@recipe_router.post("/recipes/{recipe_id}/like")
@limiter.limit("30/min")
async def like_unlike_recipe(
    request: Request,
    recipe_id: UUID,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
    """
    Fetch a specific recipe by its name and UUID.
    Rate-limited to 30 requests per minute.
    """
    try:
        await service.like_unlike( user.id,recipe_id)
        return {
            "success": True,
        }
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch recipe.")    
    
    
@recipe_router.post("/recipes/{recipe_id}/favourite-recipe")
@limiter.limit("30/min")
async def save_unsave_favourite_recipe(
    request: Request,
    recipe_id: UUID,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
    """
    Fetch a specific recipe by its name and UUID.
    Rate-limited to 30 requests per minute.
    """
    try:
        await service.like_unlike_favourite( user.id,recipe_id)
        return {
            "success": True,
        }
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch recipe.")   
    
    
    
@recipe_router.get("/recipe/meta")
@limiter.limit("30/min")
async def recipe_meta(
    request: Request,
    recipe_id: UUID,
    name:str,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
    """
    Fetch a specific recipe by its name and UUID.
    Rate-limited to 30 requests per minute.
    """
    try:
        meta = await service.get_recipe_meta( recipe_id,user.id)
        return meta
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch recipe.") 
          


class RecipesMetaRequest(BaseModel):
    recipe_ids: List[UUID]

@recipe_router.post("/recipes/meta")
@limiter.limit("30/min")
async def fetch_recipes_meta(
    request: Request,
    payload: RecipesMetaRequest,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
    """
    Fetch metadata (like, is_saved, etc.) for a list of recipes by their UUIDs.
    Rate-limited to 30 requests per minute.
    """
    try:
        if not payload.recipe_ids:
            raise HTTPException(status_code=400, detail="No recipe IDs provided.")

        metas = await asyncio.gather(*[
            service.get_recipe_meta(recipe_id, user.id)
            for recipe_id in payload.recipe_ids
        ])

        result = {}

        for i, meta in enumerate(metas):
            if meta:
                result[str(payload.recipe_ids[i])] = meta

        return result

    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch recipe.")
     
        
    
@recipe_router.get("/recipes/comments")
@limiter.limit("30/min")
async def fetch_comments(
    request: Request,
    recipe_id: UUID,
    parent:Optional[int]=None,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
    """
    Fetch a specific recipe by its name and UUID.
    Rate-limited to 30 requests per minute.
    """
    try:
        print("recipe_id received:", recipe_id)
        comments = await service.get_comments(recipe_id,parent,user.id,10,0)
        return comments
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch comments.")



class RecipeCommentRequest(BaseModel):
    comment_id: Optional[int] = None  # For editing
    content: str
    file: Optional[str] = None        # Assuming it's a file URL or base64 string
    parent: Optional[int] = None   # For replying to a comment

    
@recipe_router.post("/recipes/{recipe_id}/comments")
@limiter.limit("30/min")
async def post_recipe_comments(
    request: Request,
    recipe_id: UUID,
    data: RecipeCommentRequest,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
    """
    Create, reply to, or edit a comment on a specific recipe.

    - Rate-limited to 30 requests per minute.
    - If `comment_id` is provided, the comment will be edited.
    - If `parent_id` is provided (but not `comment_id`), it will be treated as a reply.
    - Otherwise, a new top-level comment will be created.
    """
    try:
        if data.comment_id:
            # Edit existing comment
            return await service.edit_comment(user.id, data.comment_id, data.content)

        if data.parent:
            # Reply to a comment
            return await service.reply_to_comment(user.id, recipe_id, data.parent, data.content)

        # Post a new top-level comment
        return await service.post_comment(user.id, recipe_id, data.content)

    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process comment.")
     
     
@recipe_router.delete("/recipes/{recipe_id}/comments/{comment_id}")
@limiter.limit("30/min")
async def delete_recipe_comment(
    request: Request,
    recipe_id: UUID,
    comment_id: int,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
    """
    Delete a comment on a specific recipe.
    """
    try:
        return await service.delete_comment(user.id, comment_id)

    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete comment.")




@recipe_router.post("/recipes/{recipe_name}/suggestions")
@limiter.limit("30/min")
async def suggestions_recipe(
    request: Request,
    recipe_name: str,
    service: RecipeService = Depends()
):
    """
    Delete a comment on a specific recipe.
    """
    try:
        r = await service.get_recipes_suggestions(recipe_name)
        return r
    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to get  suggestions.")



class LikeCommentRequest(BaseModel):
    id: int
    reaction: dict
    recipe_id:str   
    is_liked: bool
    
@recipe_router.post("/recipes/comments/likes")
@limiter.limit("30/min")
async def like_unlike_comments(
    request: Request,
    data: LikeCommentRequest,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
    """
    Like or unlike a comment on a recipe.
    """
    try:
        result = await service.like_unlike_comment(
            user_id=user.id,
            recipe_id=UUID(data.recipe_id),
            comment_id=data.id,
            is_liked=data.is_liked,
            reaction=data.reaction
        )
        return result
    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        print(f"[Comment Like Error] {e}")
        raise HTTPException(status_code=500, detail="Failed to like or unlike comment.")



@recipe_router.get("/recipes/views")
@limiter.limit("30/min")
async def get_viewers(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    recipe_id: UUID =None,
    user_id:Optional[UUID] = None,
    service: RecipeService = Depends()
):
    try:
        viewers= await service.get_viewers(recipe_id=recipe_id,user_id=user_id, offset=offset,limit=limit)
        return viewers
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
