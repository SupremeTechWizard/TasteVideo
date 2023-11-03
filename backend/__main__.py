from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import crud, models, schemas
from .database import SessionLocal, engine

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")


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


@app.post("/CreateUser")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
