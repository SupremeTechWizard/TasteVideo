import os
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from jose import jwt, JWTError

from . import crud, models, schemas
from .database import SessionLocal, engine

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")

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


@app.middleware("http")
async def add_content_range_header(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/static"):
        response.headers["Accept-Ranges"] = "bytes"
    return response


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/GetVideos")
def get_videos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    videos = crud.get_videos(db, skip=skip, limit=limit)
    return videos


@app.post("/CreateVideo")
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    return crud.create_video(db=db, video=video)


@app.post("/CreateUser", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user, token = crud.create_user(db=db, user=user, secret_key=SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer", "email": user.email, "id": user.id}


@app.get("/SearchVideos")
def search_videos(query: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    videos = crud.search_videos(db, query=query, skip=skip, limit=limit)
    return videos


@app.post("/CreateComment")
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment)


@app.post("/CreateLike")
def create_like(like: schemas.LikeCreate, db: Session = Depends(get_db)):
    return crud.create_like(db=db, like=like)


@app.post("/Login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/VerifyToken")
def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return {"email": user.email, "id": user.id}


@app.post("/UploadVideo")
async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db),
                       token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    file_location = await crud.save_video(file, user.id)

    video_data = schemas.VideoCreate(src=file_location, category="默认分类", title="上传的视频", description="视频描述")
    crud.create_video(db=db, video=video_data, user_id=user.id)
    return {"info": "Video uploaded successfully", "filename": file.filename}


@app.get("/GetVideosByCategory")
def get_videos_by_category(category: str, db: Session = Depends(get_db)):
    return crud.get_videos_by_category(db, category=category)


if __name__ == "__main__":
    import uvicorn
    os.makedirs("./static/videos", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
