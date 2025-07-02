from tortoise import fields, models
from tortoise.models import Model
from fastapi_admin.models import AbstractAdmin
import uuid
from datetime import datetime


# -------------------- Admin User --------------------
class AdminUser(AbstractAdmin):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=128)
    is_superuser = fields.BooleanField(default=False)

    def __str__(self):
        return self.username


# -------------------- Users --------------------
class Users(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    email = fields.CharField(max_length=255, unique=True, index=True)
    name = fields.CharField(max_length=255)
    picture = fields.CharField(max_length=855, null=True)
    is_verified = fields.BooleanField(default=False)
    password = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)
    location = fields.CharField(max_length=180, null=True)
    user_Agent = fields.CharField(max_length=500, null=True)
    last_login = fields.DatetimeField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        table = "users"


# -------------------- Recipe Category --------------------
class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    description = fields.TextField(null=True)

    def __str__(self):
        return self.name


# -------------------- Tag --------------------
class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# -------------------- Recipe --------------------
class Recipe(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    user = fields.ForeignKeyField("models.Users", related_name="recipes")
    category = fields.ForeignKeyField("models.Category", related_name="recipes")
    tags = fields.ManyToManyField("models.Tag", related_name="recipes")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    cook_time_minutes = fields.IntField()
    image_url = fields.CharField(max_length=1024, null=True)

    def __str__(self):
        return self.title


# -------------------- Recipe Ingredient --------------------
class Ingredient(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    amount = fields.CharField(max_length=100)
    unit = fields.CharField(max_length=50)
    recipe = fields.ForeignKeyField("models.Recipe", related_name="ingredients")

    def __str__(self):
        return f"{self.amount} {self.unit} {self.name}"


# -------------------- Recipe Step --------------------
class RecipeStep(Model):
    id = fields.IntField(pk=True)
    recipe = fields.ForeignKeyField("models.Recipe", related_name="steps")
    step_number = fields.IntField()
    instruction = fields.TextField()

    def __str__(self):
        return f"Step {self.step_number} of Recipe"


# -------------------- Comment --------------------
class Comment(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users", related_name="comments")
    recipe = fields.ForeignKeyField("models.Recipe", related_name="comments")
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.name}"


# -------------------- Rating --------------------
class Rating(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users", related_name="ratings")
    recipe = fields.ForeignKeyField("models.Recipe", related_name="ratings")
    score = fields.IntField()  # 1 to 5 stars
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.score} by {self.user.name}"


# -------------------- Favorite --------------------
class Favorite(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users", related_name="favorites")
    recipe = fields.ForeignKeyField("models.Recipe", related_name="favorited_by")
    added_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "recipe")


# -------------------- Media (e.g. photos/videos) --------------------
class Media(Model):
    id = fields.IntField(pk=True)
    recipe = fields.ForeignKeyField("models.Recipe", related_name="media")
    url = fields.CharField(max_length=1000)
    media_type = fields.CharField(max_length=20)  # "image", "video"

    def __str__(self):
        return f"{self.media_type} for {self.recipe.title}"

