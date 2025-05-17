
from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime,date
import uuid
import sqlalchemy.dialects.postgresql as pg
from typing import Optional, List


class Book(SQLModel,table = True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(
       sa_column= Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    updated_at: datetime= Field(
      sa_column=  Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    user_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="user.uid"
    )
    user: Optional["User"] = Relationship(back_populates="books", sa_relationship_kwargs={'lazy':"selectin"})
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={'lazy':"selectin"})

    

class User(SQLModel, table  = True):
    __tablename__ ="user"
    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    email:str
    first_name:str
    last_name:str
    isVerified: bool = False
    password_hash: str = Field(
        exclude=True
    )
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    role:str = Field(
        sa_column=Column(
            pg.VARCHAR,
            nullable=False,
            server_default="user"
        )
    )
    books: List["Book"]= Relationship(
        back_populates="user", sa_relationship_kwargs={'lazy':"selectin"}
    )
    reviews: List["Review"]= Relationship(
        back_populates="user", sa_relationship_kwargs={'lazy':"selectin"}
    )
    
class Review(SQLModel, table=True):
    __tablename__="reviews"
    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable= False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    description: str
    rating: int = Field(lt=5)
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="user.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None,foreign_key="books.uid")
    user: Optional["User"] = Relationship(back_populates="reviews", sa_relationship_kwargs={'lazy':"selectin"})
    book: Optional["Book"] = Relationship(back_populates="reviews", sa_relationship_kwargs={'lazy':"selectin"})
    
   
    