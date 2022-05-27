from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.cruds import opinions as crud
from app.schemas import opinions as schemas
from .base import get_db, response_codes


router = APIRouter(
    prefix = "/opinions",
    tags = ["Opinion"],
)


@router.get("/", response_model = list[schemas.Opinion])
def get_opinions(skip: int = 0, limit: int = 100, album_id: int = None,
                 user_id: str = None, db: Session = Depends(get_db)):
    opinion = crud.get_opinions(db, skip = skip, limit = limit,
                                album_id = album_id, user_id = user_id)
    return opinion


@router.get("/{opinion_id}", response_model = schemas.Opinion,
            responses = {404: response_codes[404]})
def get_opinion(opinion_id: int, db: Session = Depends(get_db)):
    opinion = crud.get_opinion(db, opinion_id = opinion_id)
    if opinion is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Opinion not found")

    return opinion


@router.put("/", response_model = schemas.Opinion,
            responses = {201: {
                "description": "Created",
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "#/components/schemas/Opinion"
                        }
                    }
                }
            }})
def put_opinion(opinion: schemas.OpinionPut, response: Response,
                db: Session = Depends(get_db)):
    opinion, created = crud.put_opinion(db, opinion)
    if created:
        response.status_code = status.HTTP_201_CREATED

    return opinion


@router.delete("/{opinion_id}", response_model = schemas.Opinion,
               responses = {404: response_codes[404]})
def remove_opinion(opinion_id: int, db: Session = Depends(get_db)):
    opinion = crud.remove_opinion(db, opinion_id)
    if opinion is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Opinion not found")

    return opinion
