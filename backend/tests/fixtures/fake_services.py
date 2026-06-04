from types import SimpleNamespace
from uuid import uuid4


class FakeAuthService:
    def __init__(self):
        self.calls = []

    async def login(self, email, password):
        self.calls.append(("login", email, password))
        return {"access_token": "token", "user": {"email": email}}

    async def signup(self, email, name, password, confirm_password, terms):
        self.calls.append(("signup", email, name, password, confirm_password, terms))
        return {"id": "verification-id", "type": "email"}

    async def renew_token(self, user_id):
        self.calls.append(("renew_token", str(user_id)))
        return {"access_token": "fresh-token"}

    async def verify_code(self, code_id, code, type):
        self.calls.append(("verify_code", str(code_id), code, type))
        return {"verified": True}

    async def send_verification(self, method, user, code_id, type, new_email=None):
        self.calls.append(("send_verification", method, user, str(code_id) if code_id else None, type, new_email))
        return {"sent": True}

    async def change_password(self, verifier, password, confirm_password):
        self.calls.append(("change_password", verifier, password, confirm_password))
        return {"reset": True}

    async def is_user_exists(self, verifier):
        self.calls.append(("is_user_exists", str(verifier)))
        if verifier in ("missing@example.com", "missing-user-id"):
            return None
        if verifier == "taken@example.com":
            return SimpleNamespace(id=verifier, email=verifier)
        return SimpleNamespace(id=verifier, email=verifier if "@" in str(verifier) else f"{verifier}@example.com")

    async def follow_unfollow(self, user_id, chef_id):
        self.calls.append(("follow_unfollow", str(user_id), str(chef_id)))
        return True

    async def update_user(self, data, user):
        self.calls.append(("update_user", data.username, str(user.id)))
        return {"success": True, "user": {"username": data.username}}

    async def get_followers(self, **kwargs):
        self.calls.append(("get_followers", kwargs))
        return {"followers": [], "count": 0}

    async def get_following(self, **kwargs):
        self.calls.append(("get_following", kwargs))
        return {"following": [], "count": 0}

    async def request_chef(self, user_id):
        self.calls.append(("request_chef", str(user_id)))
        return True

    async def get_chefs_stats(self):
        self.calls.append(("get_chefs_stats",))
        return {"stats": [], "popular_chef": {}}

    async def get_chefs(self, user_id):
        self.calls.append(("get_chefs", str(user_id)))
        return {"chefs": [], "total": 0}

    async def get_user(self, username, user_id):
        self.calls.append(("get_user", username, str(user_id)))
        return {"user": {"username": username}, "userMetadata": {}}


class FakeRecipe:
    id = uuid4()


class FakeRecipeService:
    def __init__(self):
        self.calls = []

    async def create_or_update_recipe(self, data, user_id, user_name):
        self.calls.append(("create_or_update_recipe", data.recipeCover.recipeName, str(user_id), user_name))
        return FakeRecipe()

    async def list_recipes(self, **kwargs):
        self.calls.append(("list_recipes", kwargs))
        return [{"id": "recipe-1", "name": kwargs.get("name")}]

    async def get_recipe_by_id(self, name, recipe_id, user_id):
        self.calls.append(("get_recipe_by_id", name, str(recipe_id), str(user_id)))
        return {"name": name}, [{"no": 1}]

    async def like_unlike(self, user_id, recipe_id):
        self.calls.append(("like_unlike", str(user_id), str(recipe_id)))

    async def like_unlike_favourite(self, user_id, recipe_id):
        self.calls.append(("like_unlike_favourite", str(user_id), str(recipe_id)))

    async def get_recipe_meta(self, recipe_id, user_id):
        self.calls.append(("get_recipe_meta", str(recipe_id), str(user_id)))
        return {"is_liked": False, "is_saved": True}

    async def get_comments(self, recipe_id, parent, user_id, limit, offset):
        self.calls.append(("get_comments", str(recipe_id), parent, str(user_id), limit, offset))
        return {"comments": [], "count": 0}

    async def post_comment(self, user_id, recipe_id, content):
        self.calls.append(("post_comment", str(user_id), str(recipe_id), content))
        return {"id": 1, "content": content}

    async def reply_to_comment(self, user_id, recipe_id, parent, content):
        self.calls.append(("reply_to_comment", str(user_id), str(recipe_id), parent, content))
        return {"id": 2, "parent": parent}

    async def edit_comment(self, user_id, comment_id, content):
        self.calls.append(("edit_comment", str(user_id), comment_id, content))
        return {"id": comment_id, "content": content}

    async def delete_comment(self, user_id, comment_id):
        self.calls.append(("delete_comment", str(user_id), comment_id))
        return {"success": True}

    async def get_recipes_suggestions(self, recipe_name):
        self.calls.append(("get_recipes_suggestions", recipe_name))
        return [{"name": recipe_name}]

    async def like_unlike_comment(self, **kwargs):
        self.calls.append(("like_unlike_comment", kwargs))
        return {"success": True}

    async def get_viewers(self, **kwargs):
        self.calls.append(("get_viewers", kwargs))
        return {"views": []}

    async def get_likes(self, **kwargs):
        self.calls.append(("get_likes", kwargs))
        return {"likes": []}

    async def delete_recipe(self, user_id, recipe_id):
        self.calls.append(("delete_recipe", str(user_id), str(recipe_id)))
        return {"success": True}


class FakeNotificationService:
    def __init__(self):
        self.calls = []

    async def get_notifications(self, user_id, filters=None):
        self.calls.append(("get_notifications", str(user_id), filters))
        return {"notifications": [{"id": "n1", "type": "like"}], "count": 1}

    async def get_user_notifications_counts(self, user_id):
        self.calls.append(("get_user_notifications_counts", str(user_id)))
        return {"likes": 2, "comment": 1, "mentions": 0, "follows": 3, "system": 0, "all": 6}

    async def read_notification(self, noty_id):
        self.calls.append(("read_notification", str(noty_id)))
        return {"success": True, "read": True}

    async def mark_all_as_read(self, user_id, type_):
        self.calls.append(("mark_all_as_read", str(user_id), type_))
        return {"success": True, "marked": type_}

    async def delete_notification(self, noty_id):
        self.calls.append(("delete_notification", str(noty_id)))
        return {"success": True}

    async def update_notification_settings(self, user_id, data):
        self.calls.append(("update_notification_settings", str(user_id), data.email_notifications))
        return {"success": True}

    async def get_notification_settings(self, user_id):
        self.calls.append(("get_notification_settings", str(user_id)))
        return {
            "email_notifications": True,
            "push_notifications": True,
            "notificationTypes": {"like": True, "comment": True},
        }


class FakeCookingTipService:
    def __init__(self):
        self.calls = []

    async def list_cooking_tips(self, **kwargs):
        self.calls.append(("list_cooking_tips", kwargs))
        return [{"id": "tip-1", "title": kwargs.get("title") or "Quick Tip"}]
