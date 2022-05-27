from sqlalchemy.orm import Session

from app.models import opinions as models
from app.schemas import opinions as schemas


def get_opinions(db: Session, skip: int = 0, limit: int = 100,
                 album_id: int = None, user_id: str = None):
    query = db.query(models.Opinion)

    if album_id is not None:
        query = query.filter_by(album_id = album_id)
    if user_id is not None:
        query = query.filter_by(user_id = user_id)

    return query.offset(skip).limit(limit).all()


def get_opinion(db: Session, opinion_id: int):
    return db.query(models.Opinion)\
             .filter(models.Opinion.id == opinion_id)\
             .first()


def put_opinion(db: Session, opinion: schemas.OpinionPut):
    created = False
    db_opinion = db.query(models.Opinion).filter_by(
        user_id = opinion.user_id,
        album_id = opinion.album_id
    ).first()

    if db_opinion is not None:
        db_opinion.opinion = opinion.opinion
    else:
        db_opinion = models.Opinion(**opinion.dict())
        db.add(db_opinion)
        created = True

    db.commit()
    db.refresh(db_opinion)
    return db_opinion, created


def remove_opinion(db: Session, opinion_id: int):
    db_opinion = get_opinion(db, opinion_id)
    if db_opinion is None:
        return None

    db.delete(db_opinion)
    db.commit()

    return db_opinion
