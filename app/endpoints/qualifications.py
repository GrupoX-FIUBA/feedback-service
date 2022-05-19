from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.cruds import qualifications as crud
from app.schemas import qualifications as schemas
from .base import get_db, response_codes


router = APIRouter(
    prefix = "/qualifications",
    tags = ["Qualification"],
)


@router.get("/", response_model = list[schemas.Qualification])
def get_qualifications(skip: int = 0, limit: int = 100,
                       db: Session = Depends(get_db)):
    qualis = crud.get_qualifications(db, skip = skip, limit = limit)
    return qualis


@router.get("/{qualification_id}", response_model = schemas.Qualification,
            responses = {404: response_codes[404]})
def get_qualification(qualification_id: int, db: Session = Depends(get_db)):
    quali = crud.get_qualification(db, qualification_id = qualification_id)
    if quali is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Qualification not found")

    return quali


@router.post("/", response_model = schemas.Qualification,
             status_code = status.HTTP_201_CREATED)
def create_qualification(qualification: schemas.QualificationCreate,
                         db: Session = Depends(get_db)):
    return crud.create_qualification(db, qualification = qualification)


@router.patch("/{qualification_id}", response_model = schemas.Qualification,
              responses = {404: response_codes[404]})
def edit_qualification(qualification_id: int,
                       qualification: schemas.QualificationUpdate,
                       db: Session = Depends(get_db)):
    db_qualification = get_qualification(qualification_id, db)

    return crud.edit_qualification(db, qualification = db_qualification,
                                   updated_qualification = qualification)


@router.delete("/{qualification_id}", response_model = schemas.Qualification,
               responses = {404: response_codes[404]})
def remove_qualification(qualification_id, db: Session = Depends(get_db)):
    qualification = crud.remove_qualification(db, qualification_id)
    if qualification is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Qualification not found")

    return qualification
