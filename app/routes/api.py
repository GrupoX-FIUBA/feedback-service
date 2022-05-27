from fastapi import APIRouter

from app.endpoints import comments, opinions, qualifications
from app.endpoints.base import response_codes


router = APIRouter()
router.include_router(comments.router, responses = {401: response_codes[401]})
router.include_router(opinions.router, responses = {401: response_codes[401]})
router.include_router(qualifications.router,
                      responses = {401: response_codes[401]})
