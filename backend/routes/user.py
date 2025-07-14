from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr
from utils.auth import AuthService, AuthError,get_current_user
from utils.limiter import limiter  
from models import User as Users
from uuid import UUID
from typing import Optional

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



@user_router.post("/{username}")
@limiter.limit("30/min")
async def get_user(
    request: Request,
    # userId: UUID,
    username: str,
    user: Users = Depends(get_current_user),
    auth: AuthService = Depends()
):
    """
    Fetch a specific user by its UUID.
    Rate-limited to 30 requests per minute.
    """
    try:
        user_data = await auth.get_user(username,user.id)
        return user_data
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    


class UserUpdate(BaseModel):
    user_id: Optional[UUID]
    email: EmailStr
    new_email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    theme:Optional[str]=None
    website:Optional[str]=None
    
    
@user_router.post("/update/{username}")
@limiter.limit("30/min")
async def update_user(
    request: Request,
    data: UserUpdate,
    username: str,
    user: Users = Depends(get_current_user),
    auth: AuthService = Depends()
):
    """
    Update user details by username.
    Rate-limited to 30 requests per minute.
    """
    try:
        if not user:
            raise HTTPException(status_code=404, detail="Authenticated user not found")

        if user.id != data.user_id and user.email != data.email:
            raise HTTPException(status_code=400, detail="User ID or email does not match the authenticated user")

        return await auth.update_user(data,user)

    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))



@user_router.get("/followers")
@limiter.limit("30/min")
async def get_followers(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    target_id: UUID =None,
    user_id:Optional[UUID] = None,
    auth: AuthService = Depends()
):
    try:
        followers= await auth.get_followers(target_id=target_id,user_id=user_id, offset=offset,limit=limit)
        return followers
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.get("/following")
@limiter.limit("30/min")
async def get_followers(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    target_id: UUID =None,
    user_id:Optional[UUID] = None,
    auth: AuthService = Depends()
):
    try:
        followers= await auth.get_following(target_id=target_id,user_id=user_id, offset=offset,limit=limit)
        return followers
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
