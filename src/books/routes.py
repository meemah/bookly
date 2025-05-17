
from fastapi import APIRouter, Depends,status
from typing import List
from .service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.main import get_session
from .schemas import BookCreateModel, BookUpdateModel, Book, BookDetailModel
from src.user.dependencies import AccessTokenBearer

from src.user.utils import create_access_token
from fastapi.responses  import JSONResponse
from ..user.dependencies import RoleChecker
from ..response.error import BookNotFound
from ..response.success import SuccessResponse


role_checker = Depends(RoleChecker(["user","admin"]))
book_router = APIRouter()
book_service = BookService()
access_token = AccessTokenBearer()

@book_router.get("/",
    response_model=SuccessResponse[List[Book]],
  dependencies=[role_checker])
async def get_all_books(
       session: AsyncSession = Depends(get_session),
       _ = Depends(access_token)
):
    books = await book_service.get_all_books(session)
    return SuccessResponse(
            message="Books fetched successfully",
            data=books

    )

# @book_router.get("/{user_uid}")
# async def get_user_books(
#     user_uid:str,
#     session:AsyncSession = Depends(get_session),
#      _ = Depends(access_token)

# ):
#     return await book_service.get_user_books(user_uid,session)

@book_router.post(
    "/",
  
    status_code=status.HTTP_201_CREATED,
     dependencies=[role_checker]
)
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details= Depends(AccessTokenBearer())
    ):
    user_uid = token_details["user"]["user_uid"]
    new_book = await book_service.create_book(user_uid, book_data,session)
    return SuccessResponse(
            message="Book created successfully",
            data=new_book
    )
    

@book_router.put("/{book_uid}",    dependencies=[role_checker]  )
async def update_book(
    book_uid:str,
    book_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session))-> dict:
    new_book = await book_service.update_book(book_uid, book_data,session)
    if new_book is None:
        raise BookNotFound()
    else:
        return SuccessResponse(
            message="Book updated successfully",
            data=new_book
        
    )

@book_router.delete("/{book_uid}",status_code=status.HTTP_204_NO_CONTENT,   dependencies=[role_checker]  )
async def delete_book(
    book_uid:str,
    session: AsyncSession = Depends(get_session)):
    book = await book_service.delete_book(book_uid,session)
    if book is not None:
        return {}
    else:
        raise BookNotFound()
    
@book_router.get("/{book_uid}",  dependencies=[role_checker],response_model=BookDetailModel  )
async def get_book(book_uid:str,
    session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_uid,session)
    if book is not None:
        return JSONResponse(
        content=SuccessResponse(
            message="Book fetched successfully",
            data=book
        )
    )
    else:
        raise BookNotFound()
