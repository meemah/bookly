from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.user.routes import auth_router
from src.reviews.routes import review_router
from .response.error import register_all_errors
@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting")
    await init_db()
    yield 
    print("server has ended")

app = FastAPI(
    lifespan=life_span
)
register_all_errors(app=app)

app.include_router(book_router,prefix="/books")
app.include_router(auth_router,prefix="/users")
app.include_router(review_router,prefix="/reviews")