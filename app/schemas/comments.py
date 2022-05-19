from pydantic import BaseModel


class CommentBase(BaseModel):
    user_id: str
    album_id: int

    comment: str


class CommentPut(CommentBase):
    pass


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True
