from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr
from utils.auth import AuthService, AuthError,get_current_user
from utils.limiter import limiter  # Make sure it's imported from one central place

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    confirm_password: str
    terms: bool


@auth_router.post("/login")
@limiter.limit("5/minute")
async def login_user(request: Request, data: LoginRequest, auth: AuthService = Depends()):
    try:
        return await auth.login(data.email, data.password)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))


@auth_router.post("/sign-up")
@limiter.limit("5/minute")
async def signup_user(request: Request, data: SignupRequest, auth: AuthService = Depends()):
    try:
        return await auth.signup(data.email, data.name, data.password, data.confirm_password, data.terms)
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post("/logout")
@limiter.limit("5/minute")
async def logout_user(request: Request, token: str):
    try:
        return True
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
