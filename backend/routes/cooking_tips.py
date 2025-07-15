from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

from .auth import get_current_user,AuthError
from utils.limiter import limiter  
from utils.recipes import RecipeService,RecipeRequest
from utils.cooking_tips import CookingTipService
from typing import List

from tortoise.expressions import Q
from uuid import UUID
from models import User as Users
from typing import Optional
from pydantic import BaseModel
cooking_tip_router = APIRouter()




@cooking_tip_router.get("/cooking-tip")
@limiter.limit("30/min")
async def create_cooking_tip(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    public_only: bool = True,
    user_id: Optional[UUID] = None,
    saved: Optional[bool] = False,
    title: Optional[str] = None,
    category: Optional[List[str]] = None,
    is_popular: bool = True,
    service: CookingTipService = Depends()
):
    try:
        cooking_tips = await service.list_cooking_tips(public_only=public_only,
                                             limit=limit, 
                                             offset=offset,
                                             user_id=user_id,
                                             title=title,
                                             category=category,
                                             is_popular=is_popular)
                                            
        return cooking_tips
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))





@cooking_tip_router.get("/cooking-tips")
@limiter.limit("30/min")
async def fetch_cooking_tips(
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


@cooking_tip_router.get("/cooking-tips/{name}/{id}")
@limiter.limit("30/min")
async def fetch_cooking_tip_by_id(
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
    


@cooking_tip_router.post("/cooking-tip/{tip_id}/like")
@limiter.limit("30/min")
async def like_unlike_cooking_tip(
    request: Request,
    tip_id: UUID,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
    """
    Fetch a specific recipe by its name and UUID.
    Rate-limited to 30 requests per minute.
    """
    try:
        await service.like_unlike( user.id,tip_id)
        return {
            "success": True,
        }
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch recipe.")    


@cooking_tip_router.post("/cooking-tip/{recipe_id}/favourite-tip")
@limiter.limit("30/min")
async def save_unsave_favourite_tip(
    request: Request,
    tip_id: UUID,
    user: Users = Depends(get_current_user),
    service: RecipeService = Depends()
):
    """
    Fetch a specific recipe by its name and UUID.
    Rate-limited to 30 requests per minute.
    """
    try:
        await service.like_unlike_favourite( user.id,tip_id)
        return {
            "success": True,
        }
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch recipe.")   
    
    