from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
from sqlmodel import create_engine,SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
import ssl
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
ssl_context = ssl.create_default_context()
engine = AsyncEngine(
    create_engine(
        url=Config.database_url,
        echo=True,
         connect_args={"ssl": ssl_context},
    )
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session
    