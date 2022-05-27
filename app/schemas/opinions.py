from pydantic import BaseModel


class OpinionBase(BaseModel):
    user_id: str
    album_id: int

    opinion: str


class OpinionPut(OpinionBase):
    pass


class Opinion(OpinionBase):
    id: int

    class Config:
        orm_mode = True
