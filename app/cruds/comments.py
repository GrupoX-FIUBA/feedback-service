from sqlalchemy.orm import Session

from app.models import comments as models
from app.schemas import comments as schemas


def get_comments(db: Session, skip: int = 0, limit: int = 100,
                 album_id: int = None, user_id: str = None):
    query = db.query(models.Comment)

    if album_id is not None:
        query = query.filter_by(album_id = album_id)
    if user_id is not None:
        query = query.filter_by(user_id = user_id)

    return query.offset(skip).limit(limit).all()


def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment)\
             .filter(models.Comment.id == comment_id)\
             .first()


def put_comment(db: Session, comment: schemas.CommentPut):
    created = False
    db_comment = db.query(models.Comment).filter_by(
        user_id = comment.user_id,
        album_id = comment.album_id
    ).first()

    if db_comment is not None:
        db_comment.comment = comment.comment
    else:
        db_comment = models.Comment(**comment.dict())
        db.add(db_comment)
        created = True

    db.commit()
    db.refresh(db_comment)
    return db_comment, created


def remove_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment is None:
        return None

    db.delete(db_comment)
    db.commit()

    return db_comment
