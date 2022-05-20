from fastapi import APIRouter, Depends, HTTPException, Response, status
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
                       album_id: int = None, db: Session = Depends(get_db)):
    qualis = crud.get_qualifications(db, skip = skip, limit = limit,
                                     album_id = album_id)
    return qualis


@router.get("/{qualification_id}", response_model = schemas.Qualification,
            responses = {404: response_codes[404]})
def get_qualification(qualification_id: int, db: Session = Depends(get_db)):
    quali = crud.get_qualification(db, qualification_id = qualification_id)
    if quali is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Qualification not found")

    return quali


@router.put("/", response_model = schemas.Qualification,
            responses = {201: {
                "description": "Created",
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "#/components/schemas/Qualification"
                        }
                    }
                }
            }}
)
def put_qualification(qualification: schemas.QualificationPut,
                      response: Response, db: Session = Depends(get_db)):
    qualification, created = crud.put_qualification(db, qualification)
    if created:
        response.status_code = status.HTTP_201_CREATED

    return qualification


@router.delete("/{qualification_id}", response_model = schemas.Qualification,
               responses = {404: response_codes[404]})
def remove_qualification(qualification_id: int, db: Session = Depends(get_db)):
    qualification = crud.remove_qualification(db, qualification_id)
    if qualification is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Qualification not found")

    return qualification


@router.get("/stats/{album_id}", responses = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    "count": 2,
                    "sum": 4,
                    "avg": 2
                }
            }
        }
    }, 404: response_codes[404]})
def album_stats(album_id: int, db: Session = Depends(get_db)):
    total = crud.sum_by_album(db, album_id)

    if total[0] is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "No qualifications for that album")

    return total
