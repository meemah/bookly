from sqlmodel import SQLModel, Field, Column
from datetime import datetime,date
import uuid
import sqlalchemy.dialects.postgresql as pg

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
    