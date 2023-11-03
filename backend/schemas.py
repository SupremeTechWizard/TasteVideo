from pydantic import BaseModel


class VideoBase(BaseModel):
    src: str
    category: str


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    text: str
    user_id: int
    video_id: int


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True


class LikeBase(BaseModel):
    user_id: int
    video_id: int


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int

    class Config:
        orm_mode = True
