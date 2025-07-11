from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

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




@recipe_router.get("/recipes")
@limiter.limit("30/min")
async def fetch_recipe(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    public_only: bool = True,
    service: RecipeService = Depends()
):
    try:
        recipes = await service.list_recipes(limit=limit, offset=offset, public_only=public_only)
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
    
    
    
@recipe_router.get("/recipes/meta")
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
        comments = await service.get_comments(recipe_id,parent,10,0)
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
     