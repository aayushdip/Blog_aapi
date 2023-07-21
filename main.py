from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import engine
import models
from hashing_password import hash_password 
from models import User, Post
from schemas import  UserCreate, PostCreate, PostUpdate, UserRead, PostRead, Token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from dependencies import get_db, settings, create_access_token, authenticate_user, get_current_user
from datetime import timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    already_existing_user = db.query(User).filter(User.email == user.email).first()
    if already_existing_user:
        raise HTTPException(status_code=400, detail="User already exists in the database")
    try:
        db_user = User(username=user.username, fullname=user.fullname, email=user.email, hashed_password=hash_password(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        print("Error caught:", e)
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/users/me", response_model=UserRead)
def read_user(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).get(user.id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except SQLAlchemyError as e:
        print("Error caught:", e)
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/posts", response_model=PostRead)
def create_post(post: PostCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        db_post = Post(
            title=post.title,
            content=post.content,
            owner_id=user.id 
        )

        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except SQLAlchemyError as e:
        print("Error caught:", e)
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/posts/{post_id}", response_model=PostRead)
def read_post(post_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        db_post = db.query(Post).get(post_id)
        if db_post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        if db_post.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to read this post")
        return db_post
    except SQLAlchemyError as e:
        print("Error caught:", e)
        raise HTTPException(status_code=500, detail="Database error")


@app.put("/posts/{post_id}", response_model=PostRead)
def update_post(post_id: int, post: PostUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        db_post = db.query(Post).get(post_id)
        if db_post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        if db_post.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this post")
        db_post.title = post.title
        db_post.content = post.content
        db.commit()
        db.refresh(db_post)
        return db_post
    except SQLAlchemyError as e:
        print("Error caught:", e)
        raise HTTPException(status_code=500, detail="Database error")


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        db_post = db.query(Post).get(post_id)
        if db_post is None:
            raise HTTPException(status_code=404, detail="Post not found")

        if db_post.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this post")

        db.delete(db_post)
        db.commit()
        return {"message": "Post deleted"}
    except SQLAlchemyError as e:
        print("Error caught:", e)
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
