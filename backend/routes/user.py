from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr
from utils.auth import AuthService, AuthError,get_current_user
from utils.limiter import limiter  
from models import User as Users
from uuid import UUID

user_router = APIRouter(prefix="/users", tags=["User"])

@user_router.post("/{chefId}/follow")
@limiter.limit("30/min")
async def recipe_meta(
    request: Request,
    chefId: UUID,
    user: Users = Depends(get_current_user),
    auth: AuthService = Depends()
):
    """
    Fetch a specific recipe by its name and UUID.
    Rate-limited to 30 requests per minute.
    """
    try:
        await auth.follow_unfollow(user.id,chefId)
        return {
            "success": True,
        }
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch recipe.")       
