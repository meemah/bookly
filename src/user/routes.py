from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreateModel, UserLoginModel
from ..db.main import get_session
from .service import UserService
from datetime import timedelta
from .utils import create_access_token,verify_password
from fastapi.responses  import JSONResponse
from src.db.redis import add_jti_to_blocklist
from .dependencies import AccessTokenBearer, get_current_user, RefreshTokenBearer
from datetime import datetime
auth_router = APIRouter()
user_service = UserService()
@auth_router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_model:  UserCreateModel, 
    session: AsyncSession = Depends(get_session),
   
):
    does_user_exist = await user_service.does_user_exist(user_model.email, session)
    if does_user_exist:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="User Account exist")
    else:
        user = await user_service.create_user(user_model,session)
        return user
     

@auth_router.post("/login")
async def login_user(
    login_model: UserLoginModel,
    session: AsyncSession = Depends(get_session)     
):
    email = login_model.email
    password = login_model.password
    
    user = await user_service.get_user_by_email(email,session)
    if user is not None:
        password_valid =  verify_password(password,user.password_hash)
        
        if password_valid is not None:
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid),
                    "role": user.role
                }
            )
            refresh_token= create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid),
                      "role": user.role
                },
                refresh=True,
                expiry=timedelta(2)
            )
            return JSONResponse(content={
                "message":"Login Successful",
                "access_token":access_token,
                "refresh_token":refresh_token,
                # "user":user.model_dump()
            })
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid email or password"
    )
@auth_router.get("/logout")
async def revoke_token(
    token_details: dict= Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session) 
):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message":"Logout successful"
        }
    )

@auth_router.get("/me")
async def get_current_user(user= Depends(get_current_user)):
    return user


@auth_router.get("/refresh_token")
async def refresh_token(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(RefreshTokenBearer())
):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={
            "access_token": new_access_token,
        })
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")