from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid
class ReviewCreateModel(BaseModel):  
    description: str
    rating: int
    

    
class ReviewModel(ReviewCreateModel):
    uid:uuid.UUID
    user_uid: Optional[uuid.UUID] 
    book_uid: Optional[uuid.UUID] 
    created_at: datetime
    updated_at: datetime 