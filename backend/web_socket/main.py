import socketio
from utils.recipes import RecipeService
from utils.auth import AuthService, get_current_user
from models import Notification
from uuid import UUID
from datetime import datetime, timedelta
from socketio import AsyncNamespace
from utils.notification import format_notifications
from utils.logger import setup_logger

logger = setup_logger("socket")


class MainNamespace(socketio.AsyncNamespace):
    namespace = "/main"

    def on_connect(self, sid, environ):
        print(f"[Main] Connected: {sid}")

    def on_disconnect(self, sid):
        print(f"[Main] Disconnected: {sid}")

    async def on_join(self, sid, data): ...


class RecipesNamespace(socketio.AsyncNamespace):
    def __init__(self, namespace, recipe_service: RecipeService):
        super().__init__(namespace)
        self.recipe_service = recipe_service

    def on_connect(self, sid, environ):
        logger.info(f"[Recipes] Connected: {sid}")

    def on_disconnect(self, sid):
        logger.info(f"[Recipes] Disconnected: {sid}")

    async def on_get_meta(self, sid, data):
        try:
            token = data.get("token")
            recipe_id = data.get("recipe_id")
            if not recipe_id:
                logger.warning(f"[Recipes] Missing recipe_id from {sid}")
                return

            user = await get_current_user(token)
            if not user:
                logger.warning(f"[Recipes] Invalid token from {sid}")
                # return

            user_id = user.id
            recipe_meta = await self.recipe_service.get_recipe_meta(recipe_id, user_id)

            if recipe_meta:
                logger.debug(f"[Recipes] Sending meta for recipe {recipe_id}")
                await self.emit("get_meta", recipe_meta, room=sid)

        except Exception as e:
            logger.exception(f"[RecipesNamespace Error]: {e}")

    async def on_update_view(self, sid, data):
        try:
            token = data.get("token")
            recipe_id = data.get("recipe_id")
            active_time = data.get("active_time", 0)
            if not recipe_id:
                logger.warning(f"[Recipes] Missing recipe_id from {sid}")
                return

            user = await get_current_user(token)
            if not user:
                logger.warning(f"[Recipes] Invalid token from {sid}")
                return

            user_id = user.id
            recipe_meta = await self.recipe_service.update_view_activity(
                user_id, recipe_id, active_time
            )

            if recipe_meta:
                logger.debug(f"[Recipes] updated view activity  for recipe {recipe_id}")

        except Exception as e:
            logger.exception(f"[RecipesNamespace Error]: {e}")


class UsersNamespace(socketio.AsyncNamespace, AuthService):
    def __init__(self, namespace, user_service: AuthService):
        super().__init__(namespace)
        self.user_service = user_service

    async def on_connect(self, sid, environ):
        print(f"[Users] Connected: {sid}")

    async def on_join_respective(self, sid, data):
        user_id = data.get("user_id")
        user = await self.user_service.is_user_exists(user_id)
        if user:
            await self.enter_room(sid, user_id)  # Use `enter_room` instead of raw `join_room`
            logger.info(f"User {user_id} joined room {user_id}")
            
            await self.emit(
            "new_notifications",
            {"notifications": "you have joined the room"},
            room=data["user_id"],
           ) 
        
            
    async def on_check_username_availability(self, sid, data):
        try:
            username = data.get("username")
            user_id = data.get("user_id")
            logger.debug(
                f"[Users] Checking availability for username: {username} from {sid}"
            )
            if not username or not user_id:
                logger.warning(f"[Users] Missing username or user_id from {sid}")
                return

            is_available = await self.user_service.check_username_availability(
                username, user_id
            )
            await self.emit(
                "check_username_availability",
                {"username": username, "available": is_available},
                room=sid,
            )
        except Exception as e:
            logger.exception(f"[UsersNamespace Error]: {e}")





class NotificationsNamespace(socketio.AsyncNamespace, AuthService):
    def __init__(self, namespace, user_service: AuthService):
            super().__init__(namespace)
            self.user_service = user_service
            
    async def on_connect(self, sid, environ):
        print(f"[Notifications] Connected: {sid}")

    async def on_join_respective(self, sid, data):
        user_id = data.get("user_id")
        user = await self.user_service.is_user_exists(user_id)
        if user:
            await self.enter_room(sid, user_id)  # Use `enter_room` instead of raw `join_room`
            logger.info(f"User {user_id} joined room {user_id}")
            
        #     await self.emit(
        #     "new_notifications",
        #     {"notifications": "you have joined the room"},
        #     room=data["user_id"],
        #    ) 
        
    async def on_check_updates(self, sid, data):
        try:
            user_id = UUID(data.get("user_id"))
            notys = await Notification.filter(user_id=user_id, is_read=False).all()
            notifications = await format_notifications(notys)

            await self.emit(
                "new_notifications",
                {"notifications": notifications},
                room=sid,
            )
        except Exception as err:
            logger.exception("[Notifications] Failed to check updates", exc_info=err)


    async def trigger_notification(self, data: dict):
        try:
            notys = data.get("notifications", [])
            notifications = await format_notifications(notys)
            # logger.info("Emiitting notifications %s!! in room %s",notifications,data["user_id"])
            if isinstance(notifications, dict):
                notifications = [notifications]

            await self.emit(
                "new_notifications",
                {"notifications": notifications},
                room=data["user_id"],
            )
        except Exception as err:
            logger.exception("[Notifications] Failed to trigger notification", exc_info=err)

