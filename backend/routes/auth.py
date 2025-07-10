from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr
from utils.auth import AuthService, AuthError,get_current_user
from utils.limiter import limiter  # Make sure it's imported from one central place
from uuid import UUID
from typing import List, Optional, Union

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

class AutRequest(BaseModel):
    user_id:Optional[UUID]
    
    
    
@auth_router.post("/refresh")
@limiter.limit("5/minute")
async def new_token(request: Request, data: AutRequest, auth: AuthService = Depends()):
    try:
        return await auth.renew_token(data.user_id)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))


from datetime import datetime

@auth_router.post("/verify")
@limiter.limit("5/minute")
async def verify_user(
    request: Request,
    code_id: UUID,
    code: str,
    type: str,
    auth: AuthService = Depends()
):
    try:
        return await auth.verify_code(code_id=code_id, code=code, type=type)
    except HTTPException as e:
        raise e  # re-raise expected HTTPExceptions
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


@auth_router.post("/send-verification")
@limiter.limit("10/minute")
async def send_verfication(
    request: Request,
    code_id: Optional[UUID] = None,
    u_id: Optional[str] = None,
    type: str = 'email',
    method: str = 'link',
    auth: AuthService = Depends()
):
    try:
        if code_id:
            return await auth.send_verification(method, None, code_id, type)

        if u_id:
            user = await auth.is_user_exists(u_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")
            return await auth.send_verification(method, user, None, type)

        raise HTTPException(status_code=400, detail="Either auth credential found , reload the page or try again later")

    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))

@auth_router.post("/is-user-exists")
@limiter.limit("2/minute")
async def is_user_exists(
    request: Request,
    verifier: str,
    auth: AuthService = Depends()
):
    try:
        user = await auth.is_user_exists(verifier)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return True


    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))

@auth_router.post("/reset-password")
@limiter.limit("5/minute")
async def change_password(
    request: Request,
    verifier: str,
    password:str,
    confirmPassword,
    auth: AuthService = Depends()
):
    try:     
        return   await auth.change_password(verifier,password,confirmPassword)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))
    

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

