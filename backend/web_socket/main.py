import socketio
from utils.recipes import RecipeService
from utils.auth import AuthService,get_current_user

from utils.logger import setup_logger
logger = setup_logger("socket")


class MainNamespace(socketio.AsyncNamespace):
    namespace = "/main"

    def on_connect(self, sid, environ):
        print(f"[Main] Connected: {sid}")

    def on_disconnect(self, sid):
        print(f"[Main] Disconnected: {sid}")

    async def on_join(self, sid, data):
        ...




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
            recipe_meta = await self.recipe_service.update_view_activity(user_id, recipe_id, active_time)

            if recipe_meta:
                logger.debug(f"[Recipes] updated view activity  for recipe {recipe_id}")

        except Exception as e:
            logger.exception(f"[RecipesNamespace Error]: {e}")            
            
            

class UsersNamespace(socketio.AsyncNamespace):
    namespace = "/users"

    def on_connect(self, sid, environ):
        print(f"[Users] Connected: {sid}")

    async def on_status_ping(self, sid, data):
        ...

class NotificationsNamespace(socketio.AsyncNamespace):
    namespace = "/notifications"

    async def on_connect(self, sid, environ):
        print(f"[Notifications] Connected: {sid}")

    async def on_check_updates(self, sid, data):
        ...
