from pydantic import BaseModel


class QualificationBase(BaseModel):
    user_id: str
    album_id: int

    value: int


class QualificationPut(QualificationBase):
    pass


class Qualification(QualificationBase):
    id: int

    class Config:
        orm_mode = True
