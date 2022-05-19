from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.cruds import examples as crud
from app.schemas import examples as schemas
from .base import get_db, response_codes


router = APIRouter(
    prefix = "/examples",
    tags = ["Example"],
)


@router.get("/", response_model = list[schemas.Example])
def get_examples(skip: int = 0, limit: int = 100,
                 db: Session = Depends(get_db)):
    examples = crud.get_examples(db, skip = skip, limit = limit)
    return examples


@router.get("/{example_id}", response_model = schemas.Example,
            responses = {404: response_codes[404]})
def get_example(example_id: int, db: Session = Depends(get_db)):
    example = crud.get_example(db, example_id = example_id)
    if example is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Example not found")

    return example


@router.post("/", response_model = schemas.Example,
             status_code = status.HTTP_201_CREATED)
def create_example(example: schemas.ExampleCreate,
                   db: Session = Depends(get_db)):
    return crud.create_example(db, example = example)


@router.patch("/{example_id}", response_model = schemas.Example,
              responses = {404: response_codes[404]})
def edit_example(example_id: int, example: schemas.ExampleUpdate,
                 db: Session = Depends(get_db)):
    db_example = get_example(example_id, db)

    return crud.edit_example(db, example = db_example,
                             updated_example = example)


@router.delete("/{example_id}", response_model = schemas.Example,
               responses = {404: response_codes[404]})
def remove_example(example_id, db: Session = Depends(get_db)):
    example = crud.remove_example(db, example_id)
    if example is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Example not found")

    return example
