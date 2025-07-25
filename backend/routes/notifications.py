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
from utils.logger import setup_logger

logger = setup_logger("NOTIFICATION ROUTES")
notification_router = APIRouter()


class NotificationsRequest(BaseModel):
    all: Optional[bool] = None
    is_read: Optional[bool] = None
    follow: Optional[bool] = None
    like: Optional[bool] = None
    mention: Optional[bool] = None
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
    user: Users = Depends(get_current_user),
    service: NotificationService = Depends(),
):
    """
    Fetch notifications for the current user.

    - Filters by read status, type (likes, follows, mentions, system).
    - Rate-limited to 30 requests per minute.
    """
    try:
        r= await service.get_user_notifications_counts(user.id)
        return r

    except Exception as e:
        logger.exception(e)
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
        r = await service.read_notification(noty_id)
        return r

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
        r = await service.mark_all_as_read(user.id,data.type)
        return r

    except Exception as e:
        logger.exception(e)
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
        if not user:
            raise HTTPException(status_code=404, detail="user not found!")
        
        r = await service.delete_notification(noty_id)
        return r

    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Failed to fetch notifications.")


class NotificationTypes(BaseModel):
    like: Optional[bool] = True
    comment: Optional[bool] = True
    mention: Optional[bool] = True
    follow: Optional[bool] = True
    system: Optional[bool] = True

class NotificationsSettings(BaseModel):
    email_notifications: Optional[bool] = True
    push_notifications: Optional[bool] = True
    notificationTypes: NotificationTypes = NotificationTypes()
    
@notification_router.post("/notifications/settings")
@limiter.limit("30/min")
async def notifications_settings(
    request: Request,
    data: NotificationsSettings,
    user: Users = Depends(get_current_user),
    service: NotificationService = Depends(),
):
    try:
        if not user:
            raise HTTPException(status_code=404, detail="user not found!")
        
        r = await service.update_notification_settings(user.id,data)
        return r

    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Failed to fetch notifications.")



@notification_router.post("/notifications/settings/get")
@limiter.limit("30/min")
async def get_notifications_settings(
    request: Request,
    user: Users = Depends(get_current_user),
    service: NotificationService = Depends(),
):
    try:
        if not user:
            raise HTTPException(status_code=404, detail="user not found!")
        
        r = await service.get_notification_settings(user.id)
        return r

    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Failed to fetch notifications.")
