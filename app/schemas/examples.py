from typing import Optional

from pydantic import BaseModel


class ExampleBase(BaseModel):
    name: str


class ExampleCreate(ExampleBase):
    pass


class ExampleUpdate(ExampleBase):
    name: Optional[str]


class Example(ExampleBase):
    id: int

    class Config:
        orm_mode = True
