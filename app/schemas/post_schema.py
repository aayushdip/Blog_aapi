from pydantic import BaseModel
from typing import Optional
from app.schemas.user_schema import UserRead


# Pydantic model for creating a new post
class PostCreate(BaseModel):
    title: str
    content: str
    owner_id: int


# Pydantic model for updating an existing post
class PostUpdate(BaseModel):
    title: str
    content: str


# Pydantic model for reading a post
class PostRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: Optional[str]
    updated_at: Optional[str]
    author: UserRead

    class Config:
        orm_mode = True
