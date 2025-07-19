from models import Notification
from uuid import UUID

class NotificationService:
    def __init__(self, recipe_repo=Notification):
        self.recipe_repo = recipe_repo

    async def get_notifications(self, user_id: UUID, filters: dict):
        query = Notification.filter(user_id=user_id)

        if 'is_read' in filters:
            query = query.filter(is_read=filters['is_read'])
        if filters.get("likes"):
            query = query.filter(notification_type="like")
        if filters.get("follows"):
            query = query.filter(notification_type="follow")
        if filters.get("mentions"):
            query = query.filter(notification_type="mention")
        if filters.get("system"):
            query = query.filter(notification_type="system")

        if filters.get("all"):
            return await query.order_by("-created_at").all()

        return await query.order_by("-created_at").limit(20)
