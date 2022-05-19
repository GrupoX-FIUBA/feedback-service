from sqlalchemy.orm import Session

from app.models import examples as models
from app.schemas import examples as schemas


def get_examples(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Example).offset(skip).limit(limit).all()


def get_example(db: Session, example_id: int):
    return db.query(models.Example).filter(models.Example.id == example_id)\
             .first()


def create_example(db: Session, example: schemas.ExampleCreate):
    db_example = models.Example(**example.dict())
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return db_example


def edit_example(db: Session, example: schemas.Example,
                 updated_example: schemas.ExampleUpdate):
    for key, value in updated_example.dict(exclude_unset = True).items():
        setattr(example, key, value)

    db.commit()
    db.refresh(example)
    return example


def remove_example(db: Session, example_id: int):
    db_example = get_example(db, example_id)
    if db_example is None:
        return None

    db.delete(db_example)
    db.commit()

    return db_example
