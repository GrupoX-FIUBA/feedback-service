from fastapi import APIRouter

from app.endpoints import qualifications
from app.endpoints.base import response_codes


router = APIRouter()
router.include_router(qualifications.router,
                      responses = {401: response_codes[401]})
