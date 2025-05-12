
from pydantic import BaseModel, Field

class UserCreateModel(BaseModel):
    first_name: str= Field(min_length=2)
    last_name: str = Field(min_length=2)
    username: str = Field(max_length=8)
    email:str= Field(max_length=40)
    password: str = Field(min_length=6)
    
class UserLoginModel(BaseModel):
    email:str
    password:str