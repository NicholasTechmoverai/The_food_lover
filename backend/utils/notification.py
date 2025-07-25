from models import Notification, Recipe ,NotificationsSettings
from uuid import UUID
import asyncio
from typing import Optional
from datetime import datetime
from .logger import setup_logger
from config import BASE_SERVER
from tortoise.exceptions import DoesNotExist

logger = setup_logger("NOTIFICATIONS")

async def format_notifications(notys):
    logger.info(notys)
    try:
        if not isinstance(notys, list):
            notys = [notys]

        formatted = []
        for noty in notys:
            try:
                target = None

                # Check for recipe related notification
                if noty.notification_type in ['comment', 'like','recipe','new_recipe']:
                    recipe_id = noty.target_object_id if isinstance(noty.target_object_id, str) else noty.parent_notification_id
                    if recipe_id:
                        # logger.info("found recipe id")
                        recipe = await Recipe.get_or_none(id=recipe_id)
                        if recipe:
                            target = recipe
                            # logger.info("found recipe %s",recipe)


                actor = noty.actor

                image_url = ""
                if target:
                    if target.cover_image_url.startswith("https://"):
                        image_url = target.cover_image_url
                    else:
                        image_url = f"{BASE_SERVER}/{target.cover_image_url}"

                formatted.append({
                    "id": str(noty.id),
                    "type": noty.notification_type,
                    "actor": {
                        "id": str(actor.id) if actor else None,
                        "username": getattr(actor, "username", "System"),
                        "avatar": actor.picture_url if actor and actor.picture_url.startswith("https://") else f"{BASE_SERVER}/{actor.picture_url}" if actor and actor.picture_url else ""
                    },
                    "verb": noty.verb,
                    "preview": noty.preview or "",
                    "target": {
                        "id": str(noty.target_object_id) if noty.target_object_id else None,
                        "image": image_url
                    },
                    "thread_id": str(noty.thread_id) if noty.thread_id else None,
                    "second_target_object_id" : noty.second_target_object_id,
                    "read": noty.is_read,
                    "created_at": noty.created_at.isoformat() if noty.created_at else datetime.utcnow().isoformat(),
                    "meta": noty.metadata or {},
                    "url": f"/recipes/{getattr(target, 'name', '').strip().lower().replace(' ','-')}/{getattr(target, 'id', '')}" if target else None
                })

            except Exception as inner_err:
                logger.warning(f"Error formatting a single notification: {inner_err}")
                continue

        return formatted

    except Exception as err:
        logger.exception(f"Error formatting notifications list: {err}")
        return []





class NotificationService:
    def __init__(self, noty_repo=Notification):
        self.noty_repo = noty_repo
        

    async def get_user_notifications_counts(self, user_id: UUID) -> dict:
        try:
            query = self.noty_repo.filter(user_id=user_id,is_read=False)

            like_q = query.filter(notification_type="like").count()
            follow_q = query.filter(notification_type="follow").count()
            comment_q = query.filter(notification_type="comment").count()
            system_q = query.filter(notification_type="system").count()
            all_q = query.count()

            like_count, follow_count, comment_count, system_count, all_count = await asyncio.gather(
                like_q, follow_q, comment_q, system_q, all_q
            )

            return {
                "likes": like_count,
                "comment": comment_count,
                "mentions": comment_count,  # same as comment_count unless you distinguish later
                "follows": follow_count,
                "system": system_count,
                "all": all_count
            }

        except Exception as err:
            logger.exception("ERROR IN GETTING NOTIFICATIONS: %s", err)
            return {
                "likes": 0,
                "comment": 0,
                "mentions": 0,
                "follows": 0,
                "system": 0,
                "all": 0
            }


    async def get_notifications(self, user_id: UUID, filters: dict):
        try:
            query = self.noty_repo.filter(user_id=user_id).prefetch_related("user","actor")
            
            logger.info(filters)

            if 'is_read' in filters:
                query = query.filter(is_read=filters['is_read'])

            if filters.get("like"):
                query = query.filter(notification_type="like")

            if filters.get("follow"):
                query = query.filter(notification_type="follow")

            if filters.get("mention"):
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
            logger.exception("ERROR IN GETTING NOTIFICATIONS: %s", err)
            return []

    async def read_notification(self, id: UUID):
        try:
            noty = await self.noty_repo.get(id=id)
            noty.is_read = True
            await noty.save()
            return True
        except DoesNotExist:
            return {"status": "error", "message": "Notification not found."}
        except Exception as err:
            logger.exception("ERROR READING NOTIFICATION: %s", err)
            return {"status": "error", "message": "Failed to read notification."}

    async def delete_notification(self, id: UUID):
        try:
            noty = await self.noty_repo.get(id=id)
            await noty.delete()
            return {"status": "success", "message": "Notification deleted."}
        except DoesNotExist:
            return {"status": "error", "message": "Notification not found."}
        except Exception as err:
            logger.exception("ERROR DELETING NOTIFICATION: %s", err)
            return {"status": "error", "message": "Failed to delete notification."}


    async def mark_all_as_read(self, user_id: UUID, type: Optional[str] = None):
        try:
            query = self.noty_repo.filter(user_id=user_id, is_read=False)
            if type  and type != "all":
                query = query.filter(notification_type=type)

            await query.update(is_read=True)
            return {"status": "success", "message": "All notifications marked as read."}
        except Exception as err:
            logger.exception("ERROR MARKING NOTIFICATIONS AS READ: %s", err)
            return {"status": "error", "message": "Failed to mark notifications as read."}

    async def get_notification_settings(self, user_id: UUID):
        try:
            settings = await NotificationsSettings.get_or_none(user_id=user_id)
            if not settings:
                return None

            return {
                "email_notifications": settings.email_notifications,
                "push_notifications": settings.push_notifications,
                "notificationTypes": {
                    "like": settings.like,
                    "comment": settings.comment,
                    "mention": settings.mention,
                    "follow": settings.follow,
                    "system": settings.system,
                }
            }

        except Exception as err:
            logger.exception("ERROR FETCHING SETTINGS: %s", err)
            return None

    async def update_notification_settings(self, user_id: UUID, data: dict):
        try:
            settings, _ = await NotificationsSettings.get_or_create(user_id=user_id)

            data_dict = data.dict()
            print(data_dict)

            for key, value in data_dict.items():
                if key == "notificationTypes":
                    for n_key, n_value in value.items():
                        if hasattr(settings, n_key):
                            setattr(settings, n_key, n_value)
                elif hasattr(settings, key):
                    setattr(settings, key, value)

            await settings.save()
            return {"status": "success", "message": "Notification settings updated."}
        except Exception as err:
            logger.exception("ERROR UPDATING SETTINGS: %s", err)
            return {"status": "error", "message": "Failed to update notification settings."}


