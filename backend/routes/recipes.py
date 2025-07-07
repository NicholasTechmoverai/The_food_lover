from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

from .auth import get_current_user
from utils.limiter import limiter  
from utils.recipes import RecipeService,RecipeRequest

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

   
    recipe = await service.create_recipe(data, user.id)
    # return {"message": "Recipe created", "recipe_id": recipe.id}


    # Store to DB (if implemented)
    return JSONResponse({
        "message": "Recipe processed successfully",
        "user": user.name,
        "recipeName": data.recipeCover.recipeName
    })

