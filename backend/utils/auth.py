import random
from datetime import datetime, timedelta
from typing import Optional, Dict
from tortoise.expressions import Q
import os
import re
from pathlib import Path

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError, jwt
from passlib.context import CryptContext
from typing import List, Dict

from models import (
    User as Users,
    Follow,
    VerificationCode,
    Recipe,
    ChefRequest,
    Notification,
)
from config import Config, WEB_SERVER, BASE_SERVER
from utils.email_sender import (
    send_email,
    form_email_message,
    code_template,
    verify_link_template,
)
from reusables.main import sanitizeContents, save_base64_image, sanitize_name
from uuid import UUID
import secrets
from datetime import timezone

datetime.now(timezone.utc)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme to extract Bearer token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

defaultAvatar = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

from .logger import setup_logger

logger = setup_logger("AUTH")


# Dependency: Extracts user from token
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Users:
    try:
        # print("Token::",token)
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="Invalid token: missing subject"
            )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid")

    user = await Users.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_verified:
        raise HTTPException(status_code=401, detail="User unverified!!")

    return user


class AuthError(Exception):
    """Custom exception for authentication-related issues."""

    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)


class AuthService:
    def __init__(self, user_repo=Users):
        self.user_repo = user_repo

    async def renew_token(self, user_id) -> dict:
        user = await self.user_repo.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return self.generate_token(user)

    async def login(self, email: str, password: str) -> dict:
        user = await self.user_repo.get_or_none(email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not self.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        return self.generate_token(user)

    async def is_user_exists(self, verifier: str):
        user = await self.user_repo.get_or_none(Q(email=verifier) | Q(id=verifier))
        if not user:
            return None
        return user

    async def check_username_availability(
        self, username: str, user_id: UUID = None
    ) -> bool:
        if not username or not re.fullmatch(r"^[a-zA-Z0-9_]{3,20}$", username):
            return False

        # Check for existing user with that username
        user = await self.user_repo.get_or_none(username=username)

        # If user exists and it's not the same user (editing), it's taken
        if user:
            if user_id and user.id == user_id:
                return True  # allowed to keep current username
            return False  # taken by another user

        return True  # available

    async def get_user(self, username: str, my_user_id: Optional[UUID] = None) -> dict:
        try:
            user = await self.user_repo.get_or_none(username=username)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Initialize metadata
            is_following = False
            following_count = 0
            follower_count = 0
            recipes_count = 0

            try:
                if my_user_id:
                    is_following = await Follow.filter(
                        follower_id=my_user_id, following_id=user.id
                    ).exists()
            except Exception as e:
                logger.warning(f"[get_user] Failed to check following status: {e}")

            try:
                # if user.is_chef:
                follower_count = await Follow.filter(following_id=user.id).count()
                following_count = await Follow.filter(follower_id=user.id).count()
                recipes_count = await Recipe.filter(user=user).count()
            except Exception as e:
                logger.warning(f"[get_user] Failed to fetch follow/recipe stats: {e}")

            return {
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "avatar": user.picture_url
                    if user.picture_url.startswith("https://")
                    else f"{BASE_SERVER}/{user.picture_url}",
                    "bio": user.bio,
                    "name": user.name,
                    "email": user.email if user.id == my_user_id else None,
                    "created_at": user.created_at.strftime("%Y-%m-%d")
                    if user.created_at
                    else None,
                    "phone_number": user.phone_number
                    if user.id == my_user_id
                    else None,
                    "website": user.website,
                    "theme": getattr(user, "theme", "#4CAF50"),
                    "is_verified": user.is_verified,
                    "is_chef": user.is_chef,
                },
                "userMetadata": {
                    "isFollowing": is_following,
                    "followers": follower_count,  # People who follow this user
                    "following": following_count,  # People this user follows
                    "recipes_count": recipes_count,
                    "starRating": 0,
                    "reviews_count": 0,
                },
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                f"[get_user] Unexpected error while retrieving user '{username}': {e}",
                exc_info=True,
            )
            raise HTTPException(status_code=500, detail="Internal server error")

    async def signup(
        self, email: str, name: str, password: str, confirm_password: str, terms: bool
    ) -> dict:
        if not terms:
            raise HTTPException(
                status_code=400, detail="You must accept terms and conditions"
            )

        if len(password) < 6:
            raise HTTPException(
                status_code=400, detail="Password must be at least 6 characters"
            )

        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        existing_user = await self.user_repo.get_or_none(email=email)
        if existing_user:
            raise HTTPException(status_code=409, detail="Email is already registered")

        hashed_password = pwd_context.hash(password)
        username = await self.create_username(name)

        user = await self.user_repo.create(
            email=email,
            name=name,
            username=username,
            password=hashed_password,
            picture_url=defaultAvatar,
        )

        return await self.send_verification("link", user, None, "email")

    async def create_username(self, name: str) -> str:
        base_username = await sanitize_name(name)

        # Try base username first
        if not await self.check_username_availability(base_username, None):
            return base_username

        # Try appending random numbers up to N attempts
        for _ in range(5):
            random_username = f"{base_username}_{random.randint(1000, 9999)}"
            if not await self.check_username_availability(random_username, None):
                return random_username

        # Final fallback (still return something, even if not ideal)
        logger.warning("Could not find available username for base: %s", base_username)
        return f"{base_username}_{random.randint(10000, 99999)}"

    async def update_user(self, data, user) -> Dict:
        try:
            user = await self.user_repo.get_or_none(id=user.id)

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Update optional fields if provided
            if data.username:
                user.username = await sanitize_name(data.username)
            if data.name:
                user.name = data.name.strip()
            if data.bio:
                data.bio = sanitizeContents(data.bio)
                user.bio = data.bio.strip()
            if data.phone_number:
                user.phone_number = data.phone_number.strip()
            if data.location:
                user.location = data.location.strip()
            if data.new_email:
                user.email = data.new_email.strip()
            if data.theme:
                user.theme = data.theme
            if data.website:
                user.website = data.website

            if data.avatar:
                image_path = await save_base64_image(data.avatar, Config.USER_PATH)
                if image_path:
                    user.picture_url = image_path

            await user.save()

            return {
                "success": True,
                "message": "User updated successfully",
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "name": user.name,
                    "email": user.email,
                    "avatar": user.picture_url
                    if user.picture_url.startswith("https://")
                    else f"{BASE_SERVER}/{user.picture_url}",
                    "bio": user.bio,
                    "phone_number": user.phone_number,
                    "location": user.location,
                    "website": user.website,
                    "theme": getattr(user, "theme", "#4CAF50"),
                    "isVerified": user.is_verified,
                    "isChef": user.is_chef,
                },
            }

        except Exception as err:
            logger.exception(f"[update_user error]: {err}")
            raise HTTPException(
                status_code=500, detail="An error occurred while updating the user."
            )


    async def follow_unfollow(self, user_id: UUID, chef_id: UUID) -> bool:
        """
        Toggle follow/unfollow for a given chef by a user.

        Returns:
            True if followed, False if unfollowed.
        """
        try:
            follow, created = await Follow.get_or_create(
                follower_id=user_id, following_id=chef_id
            )

            if not created:
                # User already followed the chef → unfollow
                existing_notification = await Notification.get_or_none(
                    user_id=user_id,
                    actor_id=chef_id,
                    notification_type="follow",
                )
                if existing_notification:
                    await existing_notification.delete()
                await follow.delete()
                return False

            # Followed just now → send notification to the chef
            noty = await Notification.create(
                user_id=chef_id,
                actor_id=user_id,
                notification_type="follow",
                target_object_id=None,
                target_content_type="user",
                verb="followed you",
                thread_id=None,
                preview="started following you.",
            )

            # Try to import and trigger WebSocket notification
            try:
                from app import notifications_namespace
                await notifications_namespace.trigger_notification({
                        "user_id": str(chef_id),
                        "notifications": [noty],
                    })

            except ImportError as e:
                # Optionally log this exception
                print(f"WebSocket notification import failed: {e}")

            return True
        
        except Exception as err:
            logger.exception(err)


    async def get_followers(
        self, target_id: UUID, user_id: UUID, offset: int = 0, limit: int = 10
    ) -> dict:
        logger.info("followers with offfset and limit, %s ,%s", offset, limit)
        # Get paginated followers
        follows = (
            await Follow.filter(following_id=target_id)
            .offset(offset)
            .limit(limit)
            .prefetch_related("follower")
        )

        result = []

        # Extract all follower user objects
        follower_users = [f.follower for f in follows if f.follower]
        follower_ids = [u.id for u in follower_users]

        # Check which followers are followed by user_id
        following_ids = []
        if user_id:
            following_ids = await Follow.filter(
                follower_id=user_id, following_id__in=follower_ids
            ).values_list("following_id", flat=True)
            following_ids = set(following_ids)

        for follower in follower_users:
            result.append({
                "id": str(follower.id),
                "name": getattr(follower, "name", "Unknown"),
                "username": getattr(follower, "username", "unknown"),
                "isChef": follower.is_chef,
                "avatar": (
                    follower.picture_url
                    if follower.picture_url.startswith("https://")
                    else f"{BASE_SERVER}/{follower.picture_url}"
                )
                if getattr(follower, "picture_url", None)
                else "",
                "isFollowing": follower.id in following_ids,
            })

        return {
            "followers": result,
            "offset": offset,
            "limit": limit,
            "count": len(result),
        }

    async def get_following(
        self,
        target_id: UUID,  # user whose "following" list we want
        user_id: UUID,  # viewer (used for isFollowing check)
        offset: int = 0,
        limit: int = 10,
    ) -> Dict[str, List[dict]]:
        # Get paginated users the target is following
        logger.info("followings with offfset and limit, %s ,%s", offset, limit)

        follows = (
            await Follow.filter(follower_id=target_id)
            .offset(offset)
            .limit(limit)
            .prefetch_related("following")
        )

        result = []

        following_users = [f.following for f in follows if f.following]
        following_ids = [u.id for u in following_users]

        # Check which of these the viewer is also following
        is_following_back_ids = []
        if user_id:
            is_following_back_ids = await Follow.filter(
                follower_id=user_id, following_id__in=following_ids
            ).values_list("following_id", flat=True)
            is_following_back_ids = set(is_following_back_ids)

        for user in following_users:
            result.append({
                "id": str(user.id),
                "name": getattr(user, "name", "Unknown"),
                "username": getattr(user, "username", "unknown"),
                "isChef": user.is_chef,
                "avatar": (
                    user.picture_url
                    if user.picture_url.startswith("https://")
                    else f"{BASE_SERVER}/{user.picture_url}"
                )
                if getattr(user, "picture_url", None)
                else "",
                "isFollowing": user.id in is_following_back_ids,
            })

        return {
            "following": result,
            "offset": offset,
            "limit": limit,
            "count": len(result),
        }

    async def save_verification_code(self, user_id, code, verification_type):
        expiry = datetime.utcnow() + timedelta(minutes=10)

        return await VerificationCode.create(
            user_id=user_id,
            code=code,
            verification_type=verification_type,
            expires_at=expiry,
        )

    async def verify_code(self, code_id: UUID, code: str, type: str):
        verification = await VerificationCode.get_or_none(
            id=code_id, code=code, verification_type=type
        ).prefetch_related("user")

        if not verification:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This verification link is invalid or no longer exists.",
            )

        # Use timezone-aware datetime for comparison
        if verification.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This verification code has already expired.",
            )

        user = await verification.user.first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user is associated with this verification code.",
            )

        verification.is_used = True
        await verification.save()

        user = await self.user_repo.get_or_none(id=verification.user_id)
        user.is_verified = True
        await user.save()

        await verification.delete()

        return self.generate_token(user)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def send_verification(
        self,
        method="link",
        user=None,
        code_id=None,
        verification_type="email",
        new_email: Optional[str] = None,
    ):
        if code_id:
            old_code = await VerificationCode.get_or_none(id=code_id)
            if not old_code:
                raise HTTPException(
                    status_code=404, detail="Old verification code not found."
                )

            user = await self.user_repo.get_or_none(id=old_code.user_id)
            if not user or not user.email:
                raise HTTPException(
                    status_code=404, detail="User not found or missing email."
                )

            await old_code.delete()

        if not user or not user.id:
            raise HTTPException(
                status_code=400, detail="A valid user must be provided."
            )

        new_code = await self.save_verification_code(
            user_id=user.id,
            code=self.generate_secure_code(),
            verification_type=verification_type,
        )

        verification_link = (
            f"{WEB_SERVER}/register/verify"
            f"?id={new_code.id}&code={new_code.code}&type={new_code.verification_type}"
        )

        email_body = await form_email_message(
            code_template.format(code=new_code.code)
            if method == "code"
            else verify_link_template.format(link=verification_link, code=new_code.code)
        )

        # Send email
        sent = await send_email(user.email if not new_email else new_email, email_body)
        if not sent:
            raise HTTPException(
                status_code=500, detail="Failed to send verification email."
            )

        return {
            "id": str(new_code.id),
            "type": new_code.verification_type,
        }

    async def change_password(self, verifier: str, password: str, confirmPassword: str):
        if len(password) < 6:
            raise HTTPException(
                status_code=400, detail="Password must be at least 6 characters"
            )

        if password != confirmPassword:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        user = await self.user_repo.get_or_none(Q(email=verifier) | Q(id=verifier))
        hashed_password = pwd_context.hash(password)
        user.password = hashed_password
        await user.save()

        return {"success": True}

    async def upgrade_to_chef(self, user_id: str):
        user = await self.user_repo.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        sanitized_name = await sanitize_name(user.name)

        chef_dir = os.path.join(Config.CHEF_PATH, sanitized_name)

        try:
            os.makedirs(chef_dir, exist_ok=True)
        except OSError as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to create chef directory: {str(e)}"
            )

        user.is_chef = True
        await user.save()
        
        noty = await Notification.create(
            user_id=user.id,
            actor_id=user_id,
            notification_type="system",
            target_object_id=None,
            target_content_type="user",
            verb="chef upgrade",
            thread_id=None,
            preview="You have been upgraded to chef",
        )

        # Try to import and trigger WebSocket notification
        try:
            from app import notifications_namespace
            await notifications_namespace.trigger_notification({
                    "user_id": str(user.id),
                    "notifications": [noty],
                })

        except ImportError as e:
            logger.error(f"WebSocket notification import failed: {e}")

        return {
            "success": True,
            "message": f"User '{user.name}' has been upgraded to Chef.",
            "chef_directory": chef_dir,
        }

    async def request_chef(self, chef_id: UUID) -> bool:
        try:
            await ChefRequest.create(user_id=chef_id)
            return True
        except Exception as e:
            # Log or handle the exception as needed
            logger.info(f"Error creating chef request: {e}")
            return False

    def generate_token(self, user) -> dict:
        # if not user.is_verified:
        #     raise HTTPException(status_code=401, detail="User unverified!!")

        expire = datetime.utcnow() + timedelta(
            minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {"sub": str(user.id), "email": user.email, "exp": expire}

        token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": Config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": str(user.id),
                # "email": user.email,
                "name": user.username or user.name,
                "isVerified": user.is_verified,
                "isChef": user.is_chef,
                "profilePic": user.picture_url
                if user.picture_url.startswith("https://")
                else f"{BASE_SERVER}/{user.picture_url}",
            },
        }

    def generate_secure_code(self, NO=6) -> str:
        return "".join(secrets.choice("0123456789") for _ in range(NO))
