from src.db.models import Review
from fastapi import Depends, HTTPException, status
from src.user.dependencies import  AsyncSession
from src.books.service import BookService
from src.user.service import UserService
from .schema import ReviewCreateModel
from sqlmodel import select
from ..response.error import BookNotFound, UserNotFound,ReviewNotFound
book_service = BookService()
user_service = UserService()
class ReviewsService:
    async def create_review(
        self,
        user_email:str,
        create_model: ReviewCreateModel,
        book_uid: str,
        session:AsyncSession,
        
    ):
        try:
            book = await book_service.get_book(book_uid, session)
            user = await user_service.get_user_by_email(user_email,session)
            if not book:
                raise BookNotFound()
            if not user:
                raise UserNotFound()
            review = Review(
                **create_model.model_dump(),
                user= user,
                book=book
            )
            session.add(review)
            await session.commit()
            return review
        except Exception as e:
            raise HTTPException(
                    detail="Something went wrong",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    async def get_book_reviews(
        self,
        book_uid: str,
        session: AsyncSession
    ):
        book = await book_service.get_book(book_uid, session)
        if book is not None:
            return book
        else:
            raise BookNotFound()
    
    async def get_review(
        self,
        review_uid: str,
        session: AsyncSession
    
    ):
        statement = select(Review).filter(Review.uid == review_uid)
        result = await session.exec(statement)
        return result.first()
            
    async def delete_book_review(
        self,
        user_email:str,
        review_uid:str,
        session: AsyncSession
    ):
        review = await self.get_review(review_uid,session)
        user = await user_service.get_user_by_email(user_email,session)
        if not review:
                raise ReviewNotFound()
        if not user == review.user_uid:
                raise HTTPException(
                    detail="You cant delete this review",
                         status_code=status.HTTP_403_FORBIDDEN
                )
        await session.delete(review)
        await session.commit()
        
        
        
         