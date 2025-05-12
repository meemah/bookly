from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from .schema import UserCreateModel
from ..db.models import User
from .util import generate_passwd_hash
class UserService:
    async def create_user(self,user_model: UserCreateModel, session: AsyncSession ):
        new_user = User(
            **user_model.model_dump()
        )
        new_user.password_hash = generate_passwd_hash(user_model.password)
        new_user.role = "user"
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    
    async def get_users(self,session: AsyncSession):
        statement = select(User).order_by(desc(User.created_at))
        results = await session.exec(statement)
        return results.all()
        
    
    async def get_user_by_id(self, user_uid:str, session: AsyncSession):
        statement = select(User).filter(User.uid == user_uid)
        users = await session.exec(statement)
        return users.first()
    
    async def update_user(self, user_uid: str, user_model: UserCreateModel, session: AsyncSession):
        user = await self.get_user_by_id(user_uid,session)
        if user is not None:
            for k,v in user_model.model_dump().items():
                if v is not None:
                    setattr(user, k,v)
            await session.commit()
            return user
        else: 
            return None
        
    async def get_user_by_email(self, email:str, session:AsyncSession):
        statement = select(User).filter(email==User.email)
        users = await session.exec(statement)
        return users.first()
    
    async def does_user_exist(self, email:str, session:AssertionError):
        user = await self.get_user_by_email(email,session)
        return True if user is not None else None
    
    