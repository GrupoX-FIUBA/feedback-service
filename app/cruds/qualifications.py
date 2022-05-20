from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models import qualifications as models
from app.schemas import qualifications as schemas


def get_qualifications(db: Session, skip: int = 0, limit: int = 100,
                       album_id: int = None):
    query = db.query(models.Qualification)

    if album_id is not None:
        query = query.filter_by(album_id = album_id)

    return query.offset(skip).limit(limit).all()


def get_qualification(db: Session, qualification_id: int):
    return db.query(models.Qualification)\
             .filter(models.Qualification.id == qualification_id)\
             .first()


def put_comment(db: Session, qualification: schemas.QualificationPut):
    created = False
    db_quali = db.query(models.Qualification).filter_by(
        user_id = qualification.user_id,
        album_id = qualification.album_id
    ).first()

    if db_quali is not None:
        db_quali.value = qualification.value
    else:
        db_quali = models.Qualification(**qualification.dict())
        db.add(db_quali)
        created = True

    db.commit()
    db.refresh(db_quali)
    return db_quali, created


def remove_qualification(db: Session, qualification_id: int):
    db_qualification = get_qualification(db, qualification_id)
    if db_qualification is None:
        return None

    db.delete(db_qualification)
    db.commit()

    return db_qualification


def album_stats(db: Session, album_id: int):
    return db.query(
        func.count(models.Qualification.value)
            .filter(models.Qualification.album_id == album_id)
            .label("count"),
        func.sum(models.Qualification.value)
            .filter(models.Qualification.album_id == album_id)
            .label("sum"),
        func.avg(models.Qualification.value)
            .filter(models.Qualification.album_id == album_id)
            .label("avg")
    ).one_or_none()
