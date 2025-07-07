from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError, jwt
from passlib.context import CryptContext

from models import User as Users  
from config import Config


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme to extract Bearer token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# Dependency: Extracts user from token
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Users:
    try:
        print("Token::",token)
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

    return user


class AuthError(Exception):
    """Custom exception for authentication-related issues."""
    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)


class AuthService:
    def __init__(self, user_repo=Users):
        self.user_repo = user_repo

    async def login(self, email: str, password: str) -> dict:
        user = await self.user_repo.get_or_none(email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not self.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        return self.generate_token(user)

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
            password=hashed_password
        )

        return self.generate_token(user)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def generate_token(self, user) -> dict:
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
                "email": user.email,
                "name": user.name
            }
        }
