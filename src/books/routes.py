
from fastapi import APIRouter, Depends,status,HTTPException
from typing import List
from .service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.main import get_session
from .schemas import BookCreateModel, BookUpdateModel, Book
from src.user.dependencies import AccessTokenBearer, RefreshTokenBearer
from datetime import datetime
from src.user.util import create_access_token
from fastapi.responses  import JSONResponse
from ..user.dependencies import RoleChecker

role_checker = RoleChecker(["user","admin"])
book_router = APIRouter()
book_service = BookService()
access_token = AccessTokenBearer()

@book_router.get("/",response_model=List[Book],
  dependencies=role_checker               
                 
                 )
async def get_all_books(
       session: AsyncSession = Depends(get_session),
       user_details = Depends(access_token)
):
    return await book_service.get_all_books(session)


@book_router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
      dependencies=role_checker  
)
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session))-> dict:
    
    new_book = await book_service.create_book(book_data,session)
    return new_book
    

@book_router.put("/{book_uid}", response_model=Book,  dependencies=role_checker  )
async def update_book(
    book_uid:str,
    book_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session))-> dict:
    new_book = await book_service.update_book(book_uid, book_data,session)
    if new_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Not Found")
    else:
        return new_book

@book_router.delete("/{book_uid}",status_code=status.HTTP_204_NO_CONTENT,  dependencies=role_checker  )
async def delete_book(
    book_uid:str,
    session: AsyncSession = Depends(get_session)):
    book = await book_service.delete_book(book_uid,session)
    if book is not None:
        return {}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Not Found")
    
@book_router.get("/{book_uid}",  dependencies=role_checker  )
async def get_book(book_uid:str,
    session: AsyncSession = Depends(get_session)):
    return await book_service.get_book(book_uid,session)
