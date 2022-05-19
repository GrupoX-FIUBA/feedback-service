from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.cruds import comments as crud
from app.schemas import comments as schemas
from .base import get_db, response_codes


router = APIRouter(
    prefix = "/comments",
    tags = ["Comment"],
)


@router.get("/", response_model = list[schemas.Comment])
def get_comments(skip: int = 0, limit: int = 100, album_id: int = None,
                 user_id: str = None, db: Session = Depends(get_db)):
    comment = crud.get_comments(db, skip = skip, limit = limit,
                                album_id = album_id, user_id = user_id)
    return comment


@router.get("/{comment_id}", response_model = schemas.Comment,
            responses = {404: response_codes[404]})
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = crud.get_comment(db, comment_id = comment_id)
    if comment is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Comment not found")

    return comment


@router.put("/", response_model = schemas.Comment,
            responses = {201: {
                "description": "Created",
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "#/components/schemas/Comment"
                        }
                    }
                }
            }})
def put_comment(comment: schemas.CommentPut, response: Response,
                db: Session = Depends(get_db)):
    comment, created = crud.put_comment(db, comment)
    if created:
        response.status_code = status.HTTP_201_CREATED

    return comment


@router.delete("/{comment_id}", response_model = schemas.Comment,
               responses = {404: response_codes[404]})
def remove_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = crud.remove_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Comment not found")

    return comment
