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

from models import User as Users

recipe_router = APIRouter()




@recipe_router.post("/recipes")
@limiter.limit("30/min")
async def create_recipe(
    data: RecipeRequest,
    request: Request,
    user: Users = Depends(get_current_user),  # Dependency injection works here!
    service: RecipeService = Depends()
):
 
    # if not user.is_chef:
    #     raise HTTPException(status_code=403, detail="Only chefs can submit recipes")

   
    recipe = await service.create_or_update_recipe(data, user.id)
    # return {"message": "Recipe created", "recipe_id": recipe.id}


    # Store to DB (if implemented)
    return JSONResponse({
        "message": "Recipe processed successfully",
        "user": user.name,
        "recipeName": data.recipeCover.recipeName
    })



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
