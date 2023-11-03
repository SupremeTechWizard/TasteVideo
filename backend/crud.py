from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext


def get_videos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Video).offset(skip).limit(limit).all()


def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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
