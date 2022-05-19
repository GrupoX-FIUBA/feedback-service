from typing import Optional

from pydantic import BaseModel


class QualificationBase(BaseModel):
    user_id: str
    album_id: int

    value: int


class QualificationCreate(QualificationBase):
    pass


class QualificationUpdate(QualificationBase):
    value: Optional[int]


class Qualification(QualificationBase):
    id: int

    class Config:
        orm_mode = True
