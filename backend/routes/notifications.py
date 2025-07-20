from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List
import asyncio
from fastapi import Query

from .auth import get_current_user, AuthError
from utils.limiter import limiter
from utils.notification import NotificationService

from tortoise.expressions import Q
from uuid import UUID
from models import User as Users
from typing import Optional
from pydantic import BaseModel

notification_router = APIRouter()


class NotificationsRequest(BaseModel):
    all: Optional[bool] = False
    is_read: Optional[bool] = None
    follows: Optional[bool] = None
    likes: Optional[bool] = None
    mentions: Optional[bool] = None
    system: Optional[bool] = None
    offset: Optional[int] = 0
    limit: Optional[int] = 10


@notification_router.post("/notifications/{username}/fetch")
@limiter.limit("30/min")
async def fetch_user_notifications(
    request: Request,
    username: str,
    data: NotificationsRequest,
    user: Users = Depends(get_current_user),
    service: NotificationService = Depends(),
):
    """
    Fetch notifications for the current user.

    - Filters by read status, type (likes, follows, mentions, system).
    - Rate-limited to 30 requests per minute.
    """
    try:
        if not user or user.username != username:
            raise HTTPException(
                status_code=403, detail="Not authorized to fetch these notifications."
            )

        return await service.get_notifications(
            user.id, filters=data.dict(exclude_none=True)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch notifications.")


@notification_router.post("/notifications/{username}/counts")
@limiter.limit("30/min")
async def fetch_user_notifications_counts(
    request: Request,
    username: str,
    data: NotificationsRequest,
    user: Users = Depends(get_current_user),
    service: NotificationService = Depends(),
):
    """
    Fetch notifications for the current user.

    - Filters by read status, type (likes, follows, mentions, system).
    - Rate-limited to 30 requests per minute.
    """
    try:
        return {"likes": 0, "follows": 0, "all": 0}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch notifications.")



class NotificationReadRequest(BaseModel):
    read: bool


@notification_router.post("/notifications/{noty_id}/read")
@limiter.limit("30/min")
async def read_user_notifications(
    request: Request,
    noty_id: UUID,
    data: NotificationReadRequest,  # will parse from POST body
    user: Users = Depends(get_current_user),
    service: NotificationService = Depends(),
):
    try:
        # Access data.read here
        read_status = data.read
        return {"success": True, "noty_id": noty_id, "read": read_status}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch notifications.")


class NotificationAllReadRequest(BaseModel):
    type: str


@notification_router.post("/notifications/mark-all-read")
@limiter.limit("30/min")
async def mark_as_read_user_notifications(
    request: Request,
    data: NotificationAllReadRequest,  # will parse from POST body
    user: Users = Depends(get_current_user),
    service: NotificationService = Depends(),
):
    try:
        return {"success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch notifications.")

@notification_router.delete("/notifications/{noty_id}/delete")
@limiter.limit("30/min")
async def delete_user_notifications(
    request: Request,
    noty_id: UUID,
    user: Users = Depends(get_current_user),
    service: NotificationService = Depends(),
):
    try:
        # Access data.read here
        return {"success": True, "noty_id": noty_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch notifications.")
