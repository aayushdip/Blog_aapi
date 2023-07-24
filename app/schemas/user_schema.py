from pydantic import BaseModel, EmailStr


# Pydantic model for creating a new user
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    fullname: str
    password: str


# Pydantic model for reading a user
class UserRead(BaseModel):
    id: int
    fullname: str
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True


# Pydantic model for hashed password
class UserInDB(BaseModel):
    hashed_password: str

    class Config:
        orm_mode = True
