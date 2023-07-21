from pydantic import BaseModel
# Pydantic model for creating a new user
class UserCreate(BaseModel):
    email: str
    username : str
    fullname : str
    password: str


# Pydantic model for creating a new todo
class TodoCreate(BaseModel):
    title: str
    description: str
    owner_id: int


# Pydantic model for updating an existing todo
class TodoUpdate(BaseModel):
    title: str
    description: str



# Pydantic model for reading a user
class UserRead(BaseModel):
    id: int
    fullname : str
    username : str
    email: str
    is_active: bool

    class Config:
        orm_mode = True

# Pydantic model for reading a todo
class TodoRead(BaseModel):
    id: int
    title: str
    description: str
    owner: UserRead

    class Config:
        orm_mode = True

#pydantic model for hashed password
class UserInDB(BaseModel):
    hashed_password: str
    
    class Config:
        orm_mode = True
