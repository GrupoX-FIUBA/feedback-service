from sqlalchemy import Column, Integer, String, Text, UniqueConstraint

from app.db.base_class import Base


class Opinion(Base):
    id = Column(Integer, primary_key = True, index = True)

    user_id = Column(String)
    album_id = Column(Integer)

    opinion = Column(Text)

    __table_args__ = (
        UniqueConstraint("user_id", "album_id"),
    )
