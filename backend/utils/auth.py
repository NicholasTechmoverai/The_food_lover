from datetime import datetime, timedelta
from typing import Optional
from tortoise.expressions import Q
import os
import re
from pathlib import Path

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError, jwt
from passlib.context import CryptContext

from models import User as Users,Follow,VerificationCode
from config import Config,WEB_SERVER
from utils.email_sender import send_email,form_email_message,code_template,verify_link_template
from reusables.main import sanitize_name
from uuid import UUID
import secrets
from datetime import datetime, timezone
datetime.now(timezone.utc)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme to extract Bearer token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

defaultAvatar = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'


# Dependency: Extracts user from token
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Users:
    try:
        # print("Token::",token)
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing subject")
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
        user = await self.user_repo.get_or_none(
            Q(email=verifier) | Q(id=verifier)
        )
        if not user:
           return None
        return user

    async def signup(
        self, email: str, name: str,
        password: str, confirm_password: str, terms: bool
    ) -> dict:
        if not terms:
            raise HTTPException(status_code=400, detail="You must accept terms and conditions")

        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        existing_user = await self.user_repo.get_or_none(email=email)
        if existing_user:
            raise HTTPException(status_code=409, detail="Email is already registered")

        hashed_password = pwd_context.hash(password)
        user = await self.user_repo.create(
            email=email,
            name=name,
            password=hashed_password,
            picture_url=defaultAvatar
        )



        return await self.send_verification('link',user,None,'email') 
    
    async def follow_unfollow(self, user_id: UUID, chef_id: UUID) -> bool:
        """
        Toggle follow/unfollow for a given chef by a user.
        
        Returns:
            True if liked, False if unliked.
        """
        follow, created = await Follow.get_or_create(follower_id=user_id, following_id=chef_id)

        if not created:
            # Already followed → infollw it
            await follow.delete()
            return False

        # follwewd just now
        #TODO:send notifications to chef
        return True
    
    async def save_verification_code(self, user_id, code, verification_type):
        expiry = datetime.utcnow() + timedelta(minutes=10)
        
        return await VerificationCode.create(
            user_id=user_id,
            code=code,
            verification_type=verification_type,
            expires_at=expiry
        )
    
    async def verify_code(self, code_id: UUID, code: str, type: str):
        verification = await VerificationCode.get_or_none(
            id=code_id,
            code=code,
            verification_type=type
        ).prefetch_related('user')

        if not verification:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This verification link is invalid or no longer exists."
            )

        # Use timezone-aware datetime for comparison
        if verification.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This verification code has already expired."
            )

        user = await verification.user.first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user is associated with this verification code."
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
    
    async def send_verification(self, method='link', user=None, code_id=None,verification_type = 'email'):
        if code_id:
            old_code = await VerificationCode.get_or_none(id=code_id)
            if not old_code:
                raise HTTPException(status_code=404, detail="Old verification code not found.")
            
            user = await self.user_repo.get_or_none(id=old_code.user_id)
            if not user or not user.email:
                raise HTTPException(status_code=404, detail="User not found or missing email.")

            await old_code.delete()

        if not user or not user.id:
            raise HTTPException(status_code=400, detail="A valid user must be provided.")

        new_code = await self.save_verification_code(
            user_id=user.id,
            code=self.generate_secure_code(),
            verification_type=verification_type
        )

        verification_link = (
            f"{WEB_SERVER}/register/verify"
            f"?id={new_code.id}&code={new_code.code}&type={new_code.verification_type}"
        )

        email_body = await form_email_message(
            code_template.format(code=new_code.code)
            if method == 'code'
            else verify_link_template.format(link=verification_link, code=new_code.code)
        )

        # Send email
        sent = await send_email(user.email, email_body)
        if not sent:
            raise HTTPException(status_code=500, detail="Failed to send verification email.")

        return {
            "id": str(new_code.id),
            "type": new_code.verification_type,
        }

    async def change_password(self, verifier: str, password: str, confirmPassword: str):
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

        if password != confirmPassword:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        user = await self.user_repo.get_or_none(
            Q(email=verifier) | Q(id=verifier)
        )
        hashed_password = pwd_context.hash(password)
        user.password = hashed_password
        await user.save()
        
        return {"success":True}

    async def upgrade_to_chef(self, user_id: str):
        user = await self.user_repo.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        sanitized_name = await sanitize_name(user.name)

        chef_dir = os.path.join(Config.CHEF_PATH, sanitized_name)

        try:
            os.makedirs(chef_dir, exist_ok=True)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Failed to create chef directory: {str(e)}")

        user.is_chef = True
        await user.save()

        return {
            "success": True,
            "message": f"User '{user.name}' has been upgraded to Chef.",
            "chef_directory": chef_dir
        }

        
    def generate_token(self, user) -> dict:
        # if not user.is_verified:
        #     raise HTTPException(status_code=401, detail="User unverified!!")
        
        expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": expire
        }

        token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": Config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": str(user.id),
                # "email": user.email,
                "name": user.name,
                "isVerified":user.is_verified,
                "isChef":user.is_chef,
                "profilePic":user.picture_url,
            }
        }


    def generate_secure_code(self,NO=6) -> str:
        return ''.join(secrets.choice("0123456789") for _ in range(NO))
