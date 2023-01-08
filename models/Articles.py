from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Article(BaseModel):
    username: Optional[str]
    caption: str = Field(min_length=3)
    text: Optional[str] = Field(min_length=3)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    likes: int = Field(default=0)
    dislikes: int = Field(default=0)
