from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Qualification(Base):
    id = Column(Integer, primary_key = True, index = True)

    user_id = Column(String)
    album_id = Column(Integer)

    value = Column(Integer)
