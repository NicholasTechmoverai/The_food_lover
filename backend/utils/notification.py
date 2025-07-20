from models import Notification
from uuid import UUID
from datetime import datetime, timedelta
from .logger import setup_logger
logger = setup_logger("NOTIFICATIONS")
from config import Config,BASE_SERVER


async def format_notifications(notys):
    try:
        if not isinstance(notys, list):
            notys = [notys]

        formatted = []
        for noty in notys:
            actor = noty.actor
            formatted.append({
                "id": str(noty.id),
                "type": noty.notification_type,
                "actor": {
                    "id": str(actor.id) if actor else None,
                    "username": getattr(actor, "username", "System"),
                    "avatar": actor.picture_url if actor.picture_url.startswith("https://") else f"{BASE_SERVER}/{actor.picture_url}",

                },
                "verb": noty.verb,
                "preview": noty.preview or "",
                "target": {
                    "type": noty.target_content_type,
                    "id": noty.target_object_id,
                    "image": noty.image_url if noty.image_url and noty.image_url.startswith("https://") else f"{BASE_SERVER}/{noty.image_url}" if noty.image_url else "",
                },
                "thread_id": str(noty.thread_id) if noty.thread_id else None,
                "read": noty.is_read,
                "created_at": noty.created_at.isoformat() if noty.created_at else datetime.utcnow().isoformat(),
                "actions": [{"label": "View", "action": "view"}],
                "meta": noty.metadata or {}
            })

        return formatted
    
    except Exception as err:
        logger.exception(err)

    
class NotificationService:
    def __init__(self, recipe_repo=Notification):
        self.recipe_repo = recipe_repo

    async def get_notifications(self, user_id: UUID, filters: dict):
        try:
            query = Notification.filter(user_id=user_id).prefetch_related("actor")

            if 'is_read' in filters:
                query = query.filter(is_read=filters['is_read'])
            if filters.get("likes"):
                query = query.filter(notification_type="like")
            if filters.get("follows"):
                query = query.filter(notification_type="follow")
            if filters.get("mentions"):
                query = query.filter(notification_type__icontains="comment")
            if filters.get("comment"):
                query = query.filter(notification_type__icontains="comment")
            if filters.get("system"):
                query = query.filter(notification_type="system")

            if filters.get("all"):
                notys = await query.order_by("-created_at").all()
            else:
                notys = await query.order_by("-created_at").limit(20)

            return await format_notifications(notys)
        except Exception as err:
            logger.exception("ERROR IN GETTING NOTIFICATION %s",err)