from typing import Optional, List
from uuid import UUID
from models import CookingTip
from config import BASE_SERVER
from .logger import setup_logger
logger = setup_logger("socket")

class CookingTipService:
    def __init__(self, cooking_tip_repo=CookingTip):
        self.cooking_tip_repo = cooking_tip_repo

    async def list_cooking_tips(
        self,
        public_only: bool = True,
        limit: int = 10,
        offset: int = 0,
        user_id: Optional[UUID] = None,
        title: Optional[str] = None,
        category: Optional[str] = None,
        is_popular: Optional[bool] = None
    ):
        query = self.cooking_tip_repo.all().prefetch_related("user")

        if user_id:
            query = query.filter(user_id=user_id)

        if title:
            query = query.filter(title__icontains=title.strip())

        if category:
            query = query.filter(catogory__icontains=category.strip())

        if is_popular:
            query = query.filter(is_popular=True)

        query = query.order_by("-updated_at", "-created_at").offset(offset).limit(limit)
        tips = await query

        logger.info(
            "Fetched %s cooking tips | Offset: %s | Limit: %s | Title: %s | Category: %s | Popular: %s",
            len(tips), offset, limit, title, category, is_popular
        )

        result = []
        for tip in tips:
            user = getattr(tip, "user", None)

            result.append({
                "id": str(tip.id),
                "title": tip.title,
                "category": tip.catogory,
                "description": tip.content,
                "isPopular": tip.is_popular,
                "image": (
                    tip.image_url if tip.image_url and tip.image_url.startswith("https://")
                    else f"{BASE_SERVER}/{tip.image_url}" if tip.image_url else None
                ),
                "createdAt": tip.created_at.isoformat(),
                "user": {
                    "id": str(user.id) if user else None,
                    "name": getattr(user, "name", "Unknown"),
                    "username": getattr(user, "username", "Unknown"),
                    "avatar": (
                        user.picture_url if user and user.picture_url.startswith("https://")
                        else f"{BASE_SERVER}/{user.picture_url}" if user and user.picture_url else None
                    )
                }
            })

        return {
            "tips": result,
            "limit": limit,
            "offset": offset
        }
