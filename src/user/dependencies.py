from fastapi.security import HTTPBearer
from fastapi import HTTPException,status, Request, Depends
from .utils import decode_access_token
from src.db.redis import jti_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service  import UserService
from typing import List
from ..db.models import User
from ..response.error import InvalidToken, RevokedToken, AccessTokenRequired, RefreshTokenRequired,InsufficientPermission
user_service = UserService()
class TokenBearer(HTTPBearer):
    def __init__(self,auto_error = True):
        super().__init__( auto_error=auto_error)
    
    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)
        if not self.token_valid(token):
            raise InvalidToken()
        if await jti_in_blocklist(token_data['jti']):
            raise RevokedToken()
        self.verify_token_data(token_data)
        
        return token_data
   
    
    def token_valid(self,token)-> bool:
        token_data = decode_access_token(token)
        return True if token_data is not None else False
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override in child token classes")
    
        
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict)-> None:
        if  token_data and token_data["refresh"]:
            raise AccessTokenRequired()

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict)-> None:
        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequired()
        
async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
):
    user_email = token_details["user"]["email"]
    user= await user_service.get_user_by_email(user_email,session)
    return user
    
    
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: User=Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True
        else: 
            raise InsufficientPermission()