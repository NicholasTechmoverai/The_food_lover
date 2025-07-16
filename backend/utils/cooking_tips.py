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
        category: Optional[List[str]] = None,
        is_popular: Optional[bool] = None
    ):
        
        query = self.cooking_tip_repo.all().prefetch_related("user")
        total_count = await query.count()
        logger.info("Total cooking tips: %s | Offset: %s | Limit: %s", total_count, offset, limit)

        if user_id:
            query = query.filter(user_id=user_id)

        if title:
            query = query.filter(title__icontains=title)

        if category:
            query = query.filter(catogory__in=category)

        if is_popular is True:
            query = query.filter(is_popular=True)

        query = query.order_by("-updated_at", "-created_at").offset(offset).limit(limit)
        tips = await query

        result = []
        for tip in tips:
            result.append({
                "id": str(tip.id),
                "title": tip.title,
                "category": tip.catogory,
                "description": tip.content,
                "isPopular": tip.is_popular,
                "image": tip.image_url if tip.image_url.startswith("https://") else f"{BASE_SERVER}/{tip.image_url}",
                "createdAt": tip.created_at,
                "user": {
                    "id": str(tip.user.id),
                    "name": getattr(tip.user, "name", "Unknown"),
                    "username": getattr(tip.user, "username", "Unknown"),
                    "avatar":tip.user.picture_url if tip.user.picture_url.startswith("https://") else f"{BASE_SERVER}/{tip.user.picture_url}",

                    
                }
            })

        return {
            "tips": result,
            "limit": limit,
            "offset": offset
        }
