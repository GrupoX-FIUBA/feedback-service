from sqlalchemy.orm import Session

from app.models import qualifications as models
from app.schemas import qualifications as schemas


def get_qualifications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Qualification).offset(skip).limit(limit).all()


def get_qualification(db: Session, qualification_id: int):
    return db.query(models.Qualification)\
             .filter(models.Qualification.id == qualification_id)\
             .first()


def create_qualification(db: Session,
                         qualification: schemas.QualificationCreate):
    db_qualification = models.Qualification(**qualification.dict())
    db.add(db_qualification)
    db.commit()
    db.refresh(db_qualification)
    return db_qualification


def edit_qualification(db: Session, qualification: schemas.Qualification,
                       updated_qualification: schemas.QualificationUpdate):
    for key, value in updated_qualification.dict(exclude_unset=True).items():
        setattr(qualification, key, value)

    db.commit()
    db.refresh(qualification)
    return qualification


def remove_qualification(db: Session, qualification_id: int):
    db_qualification = get_qualification(db, qualification_id)
    if db_qualification is None:
        return None

    db.delete(db_qualification)
    db.commit()

    return db_qualification