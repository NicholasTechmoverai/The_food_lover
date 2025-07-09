from tortoise import fields, models
from tortoise.models import Model
from tortoise import fields
from tortoise.models import Model
from fastapi_admin.models import AbstractAdmin
from datetime import datetime
import uuid
from enum import Enum

# -------------------- Admin User --------------------

class AdminUser(AbstractAdmin):
    id = fields.IntField(pk=True)

    username = fields.CharField(max_length=50, unique=True, index=True)
    password = fields.CharField(max_length=128)
    
    is_superuser = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "admin_users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.username} ({'Superuser' if self.is_superuser else 'Staff'})"



# -------------------- Users --------------------
class User(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)

    email = fields.CharField(max_length=255, unique=True, index=True)
    name = fields.CharField(max_length=255,index=True)
    picture_url = fields.CharField(max_length=855, null=True)

    password = fields.CharField(max_length=255, null=True)
    is_verified = fields.BooleanField(default=False)
    is_chef = fields.BooleanField(default=False) 

    is_active = fields.BooleanField(default=True)
    location = fields.CharField(max_length=180, null=True)
    user_agent = fields.CharField(max_length=500, null=True)
    last_login = fields.DatetimeField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"



class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True,index=True)
    description = fields.TextField(null=True)

    class Meta:
        table = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True,index=True)
    is_popular = fields.BooleanField(default=False)  

    class Meta:
        table = "tags"
        ordering = ["-is_popular", "name"]

    def __str__(self):
        return self.name


class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
  
class CopyProtection(str, Enum):
    basic = "basic"
    restricted = "restricted"
    custom = "custom"

class Recipe(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255, index=True)
    description = fields.TextField()

    cover_image_url = fields.CharField(max_length=255)
    theme_color = fields.CharField(max_length=20)
    cuisine = fields.CharField(max_length=255, index=True)

    difficulty_level = fields.CharEnumField(Difficulty, default=Difficulty.easy, index=True)
    cook_time_minutes = fields.IntField()

    user = fields.ForeignKeyField("models.User", related_name="recipes")
    category = fields.ManyToManyField("models.Category", related_name="recipes") 
    tags = fields.ManyToManyField("models.Tag", related_name="recipes")          


    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    is_public = fields.BooleanField(default=True)
    allow_comments = fields.BooleanField(default=True)
    copy_protection = fields.CharEnumField(CopyProtection, default=CopyProtection.basic)


    class Meta:
        table = "recipes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.cuisine})"




class RecipeStep(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    recipe = fields.ForeignKeyField("models.Recipe", related_name="steps")  # assuming "Recipe" is the correct class name
    step_number = fields.IntField()  # more descriptive than "step"
    cook_time_minutes = fields.IntField(null=True)
    temperature_celsius = fields.IntField(null=True)  # optional: be specific with units
    description = fields.TextField()
    image_url = fields.CharField(max_length=255)
    video_url = fields.CharField(max_length=255,null=True)

    class Meta:
        table = "recipe_steps"
        unique_together = ("recipe", "step_number")  # ensures each step number is unique per recipe

    def __str__(self):
        return f"Step {self.step_number} of Recipe {self.recipe}"


class Ingredient(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255,index=True)
    quantity = fields.CharField(max_length=100,null=True)  # renamed from "amount"
    unit = fields.CharField(max_length=50,null=True)
    
    recipe_step = fields.ForeignKeyField("models.RecipeStep", related_name="ingredients")

    class Meta:
        table = "ingredients"
        ordering = ["recipe_step_id", "id"]

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.name}"




class RecipeComment(Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField("models.User", related_name="comments")
    recipe = fields.ForeignKeyField("models.Recipe", related_name="comments")
    content = fields.TextField()
    attachments = fields.JSONField(null=True)

    parent = fields.ForeignKeyField(
        "models.RecipeComment", related_name="replies", null=True
    )

    is_edited = fields.BooleanField(default=False)
    is_deleted = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "recipe_comments"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.name}: {self.content[:30]}"



class Rating(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="ratings")
    recipe = fields.ForeignKeyField("models.Recipe", related_name="ratings")
    score = fields.IntField()  # 1–5 star rating
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "ratings"
        unique_together = ("user", "recipe")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.score}⭐ by {self.user.name} on {self.recipe.name}"


class Favorite(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="favorites")
    recipe = fields.ForeignKeyField("models.Recipe", related_name="favorited_by")
    added_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "favorites"
        unique_together = ("user", "recipe")
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.user.name} favorited {self.recipe.name}"

class RecipeView(Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField("models.User", related_name="recipe_views")
    recipe = fields.ForeignKeyField("models.Recipe", related_name="views")

    viewed_at = fields.DatetimeField(auto_now_add=True)
    active_duration = fields.IntField(default=0)  # in seconds

    class Meta:
        table = "recipe_views"
        unique_together = ("user", "recipe")
        ordering = ["-viewed_at"]

    def __str__(self):
        return f"{self.user.name} viewed '{self.recipe.recipeName}'"


class RecipeLike(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="recipe_likes")
    recipe = fields.ForeignKeyField("models.Recipe", related_name="likes")

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "recipe_likes"
        unique_together = ("user", "recipe")

    def __str__(self):
        return f"{self.user.name} liked {self.recipe.name}"


class CommentLike(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="comment_likes")
    comment = fields.ForeignKeyField("models.RecipeComment", related_name="likes")

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "comment_likes"
        unique_together = ("user", "comment")

    def __str__(self):
        return f"{self.user.name} liked a comment"


class CookingTipLike(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="tip_likes")
    cooking_tip = fields.ForeignKeyField("models.CookingTip", related_name="likes")

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "cooking_tip_likes"
        unique_together = ("user", "cooking_tip")

    def __str__(self):
        return f"{self.user.name} liked a tip"



class ShareRecipe(models.Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField("models.User", related_name="shared_recipes")
    recipe = fields.ForeignKeyField("models.Recipe", related_name="shares")

    shared_to = fields.CharField(
        max_length=255,
        null=True,
        description="Target recipient (e.g., email, username, or platform)"
    )

    message = fields.TextField(
        null=True,
        description="Optional message included by the sharer"
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "recipe_shares"
        unique_together = ("user", "recipe", "shared_to")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        to = self.shared_to if self.shared_to else "public"
        return f"{self.user.name} shared '{self.recipe.name}' to {to} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class ShareCookingTip(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="shared_tips")
    cooking_tip = fields.ForeignKeyField("models.CookingTip", related_name="shares")

    shared_to = fields.CharField(max_length=255, null=True)
    message = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "cooking_tip_shares"
        unique_together = ("user", "cooking_tip", "shared_to")

    def __str__(self):
        return f"{self.user.name} shared a tip"


class ShareProfile(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="shared_profiles")
    target_user = fields.ForeignKeyField("models.User", related_name="profile_shared_by")

    shared_to = fields.CharField(max_length=255, null=True)
    message = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "profile_shares"
        unique_together = ("user", "target_user", "shared_to")

    def __str__(self):
        return f"{self.user.name} shared {self.target_user.name}'s profile"
        
        
class Follow(Model):
    id = fields.IntField(pk=True)

    follower = fields.ForeignKeyField("models.User", related_name="following")
    following = fields.ForeignKeyField("models.User", related_name="followers")

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "follows"
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.name} follows {self.following.name}"
    
    
    
    
class CookingTip(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)

    title = fields.CharField(max_length=255, index=True)
    content = fields.TextField()
    is_popular = fields.BooleanField(default=False, db_index=True)

    # Media
    image_url = fields.CharField(max_length=1024, null=True)
    video_url = fields.CharField(max_length=1024, null=True)

    # Author & optional related recipe
    user = fields.ForeignKeyField("models.User", related_name="cooking_tips")
    # recipe = fields.ForeignKeyField("models.Recipe", related_name="cooking_tips", null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "cooking_tips"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Tip: {self.title} by {self.user.name}"
    
#  Initialize Tortoise ORM
# from tortoise import Tortoise, run_async

# async def init():
#     await Tortoise.init(
#         db_url='mysql://root:75223031@localhost/the_food_lovers',
#         modules={'models': ['__main__']}  # Replace '__main__' with your actual module path if possible
#     )
#     await Tortoise.generate_schemas(safe=True)  # safe=True won't drop existing tables

# run_async(init())