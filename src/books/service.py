from sqlmodel import select,desc
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookUpdateModel,BookCreateModel
from ..db.models import Book


class BookService:
    async def get_all_books(self,session:AsyncSession,):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement=statement)
        
        return result.all()
    
    async def get_book(self, book_uid:str,session:AsyncSession,):
        statement = select(Book).filter(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        if book is not None:
            return book
        else:
            return None
        
    
    async def create_book(self, create_book: BookCreateModel, session:AsyncSession):
        new_book = Book(
            **create_book.model_dump()
        )
        
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book
    
    async def update_book(self,book_uid: str, update_book:BookUpdateModel,session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is not None:
            update_data_dict = update_book.model_dump()

            for k, v in update_data_dict.items():
                if v is not None:
                    setattr(book_to_update, k, v)

            await session.commit()

            return book_to_update
        else:
            return None
    
    async def delete_book(self,book_uid,session:AsyncSession):
        current_book  = await self.get_book(book_uid,session)
        if current_book is not None:
            await session.delete(current_book)
            await session.commit()
            return {}
        else:
            return None

    