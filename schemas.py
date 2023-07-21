from pydantic import BaseModel, EmailStr
from typing import Optional


# Pydantic model for creating a new user
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    fullname: str
    password: str


# Pydantic model for creating a new post
class PostCreate(BaseModel):
    title: str
    content: str
    owner_id: int


# Pydantic model for updating an existing post
class PostUpdate(BaseModel):
    title: str
    content: str


# Pydantic model for reading a user
class UserRead(BaseModel):
    id: int
    fullname: str
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True


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


# Pydantic model for hashed password
class UserInDB(BaseModel):
    hashed_password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
