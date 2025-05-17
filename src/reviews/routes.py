from fastapi import APIRouter, Depends, status
from .schema import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.user.dependencies import get_current_user, RoleChecker
from .service import ReviewsService
from src.db.models import User
from fastapi.responses  import JSONResponse
from ..response.success import SuccessResponse

review_service = ReviewsService()
review_router = APIRouter()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["user", "admin"]))

@review_router.post("/book/{book_uid}", dependencies=[user_role_checker])
async def create_review(
    book_uid:str,
    create_review_model: ReviewCreateModel,
    session: AsyncSession= Depends(get_session),
    current_user: User = Depends(get_current_user)
   
    
):
    review =  await review_service.create_review(
        current_user.email,
        create_review_model,
        book_uid,
        session ,  
    )
    return SuccessResponse(
            message="Review added",
            data=review
        
    )

@review_router.get("/book/{book_uid}", dependencies=[user_role_checker])
async def get_book_reviews(
    book_uid:str,
    session: AsyncSession= Depends(get_session),

    
):
    response = await review_service.get_book_reviews(
            book_uid,
        session
     
    )
    return SuccessResponse(
        message="Reviews fetched",
        data= response
    )