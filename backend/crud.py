from datetime import datetime, timedelta

from fastapi import UploadFile
from jose import jwt
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext


def get_videos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Video).offset(skip).limit(limit).all()


def create_video(db: Session, video: schemas.VideoCreate, user_id: int):
    db_video = models.Video(**video.dict(), user_id=user_id)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "a_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_user(db: Session, user: schemas.UserCreate, secret_key: str, algorithm: str):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires,
    )
    return db_user, access_token


def search_videos(db: Session, query: str, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Video)
        .filter(models.Video.title.ilike(f"%{query}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def create_like(db: Session, like: schemas.LikeCreate):
    db_like = models.Like(**like.dict())
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


async def save_video(file: UploadFile, user_id: int) -> str:
    file_location = f"static/videos/{user_id}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        content = await file.read()
        file_object.write(content)
    return file_location
